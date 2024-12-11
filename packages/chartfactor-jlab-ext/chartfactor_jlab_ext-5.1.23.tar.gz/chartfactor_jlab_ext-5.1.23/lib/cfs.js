import { DisposableDelegate } from '@phosphor/disposable';
import { StorageUtils } from './storage-utils';
import { getCurrent } from './commons';
import { NotebookActions } from '@jupyterlab/notebook';
import { toJSONWithDasboards } from './commons';
import { get } from 'lodash';

export default class CfsExtension {
    constructor(app, notebook) {
        this.app = app;
        this.notebook = notebook;
        this.kernel = null;
        window.syncWithStudio = true;
        window.currentApp = this.app;
        window.currentNotebook = this.notebook;
        window.souldDisplaySaveMessage = true;
    }

    createTempIframe(url = 'https://chartfactor.com/studio/jupyter.html', cell, callback) {
        let iframe = document.getElementById(cell.id);

        if (!iframe) {
            iframe = document.createElement('iframe');
            try {
                iframe.id = cell.id;
                iframe.name = cell.id;
                iframe.src = `${url}jupyter.html`;
                iframe.style.display = 'none';
                iframe.addEventListener("load", function () {
                    callback(cell, this);
                });
                document.body.appendChild(iframe);
            } catch (err) {
                console.error('Oops, unable to create the Iframe element.', err);
            }
        } else {
            callback(cell, iframe);
        }
    };

    getCellIframe(executionCount) {
        const cellIframeId = `iframe${executionCount}_${this.kernel?.id}`;
        return document.getElementById(cellIframeId);
    }

    setGlobalActiveCellId(cellId) {
        if (this.kernel) {
            this.kernel.requestExecute({
                code: `cfpy_active_cell_id = '${cellId}'`,
                silent: true
            });
        }
    }

    async onActiveCellChanged(event) {
        if (event.activeCell) {
            this.setGlobalActiveCellId(event.activeCell.model.id);
        }
    }

    getStudioAppForAllCells() {
        const notebookConfig = this.getNotebookConfig();

        for (const cell of notebookConfig.cells) {
            if (cell.cell_type === 'code') {
                const cellIFrame = this.getCellIframe(cell.execution_count);

                if (cellIFrame) {
                    cellIFrame.contentWindow.postMessage({
                        action: 'getStudioApp',
                        appId: `cfs.app-${cell.id}`
                    }, '*');
                }
            }
        }
    }

    async onSave(context, state) {
        const current = getCurrent(null, this.app, this.notebook);
        if (current) {
            if (!this.toJSON) this.toJSON = current.model.toJSON;
            switch (state) {
                case 'started':
                    if (window.syncWithStudio) {
                        this.getStudioAppForAllCells();
                    }

                    const json = current.model.toJSON(current.model);
                    current.model.toJSON = toJSONWithDasboards(json);
                    break;
                case 'completed':
                    current.model.toJSON = this.toJSON;
                    window.syncWithStudio = true;
                    window.souldDisplaySaveMessage = true;
                    delete this.toJSON;
                    break;
                default:
                    break;
            }
        }
    }

    /**
     * Receive the CFS information sent from CharFactor Studio 
     * and saves or deletes it from local Jupyter Lab storage.
     * @param {} event 
     */
    async cfsJlabSynchronizeMessageEventListener(event) {
        if (event.data.action === 'getStudioApp' && event.data.studioAppId) {
            StorageUtils.save(event.data.studioAppId, event.data.studioApp);
            StorageUtils.save('cfs.dataProviders', event.data.studioAppProviders);

            window.syncWithStudio = false;
            window.souldDisplaySaveMessage = false;
            await this.currentApp.commands.execute('docmanager:save');
        }
    }

    sendPostMessageToStudio(cell, cellIFrame) {
        // Synchronizing cell's app
        if (cell.metadata.cf_studio_app) {
            const keys = _.keys(cell.metadata.cf_studio_app);
            if (keys && keys.length > 0) {
                cell.metadata.cf_studio_app[keys[0]].creationDate = Date.now();
                cellIFrame.contentWindow.postMessage({
                    action: 'saveStudioApp',
                    storageKey: keys[0],
                    storageItem: cell.metadata.cf_studio_app[keys[0]]
                }, '*');
            }
        }

        // Synchronizing cell's providers
        if (cell.metadata.cf_studio_providers) {
            cellIFrame.contentWindow.postMessage({
                action: 'saveStudioApp',
                storageKey: 'cfs.dataProviders',
                storageItem: cell.metadata.cf_studio_providers
            }, '*');
        }

        setTimeout(() => {
            document.body.removeChild(cellIFrame);
        }, 1);
    }

    getIframeUrl(cell) {
        let iframeUrl;
        const source = cell.source.split('\n');
        source.forEach(s => {
            // Searching for a format like ".studio('My app', url='http://localhost:3333')" or 
            // ".studio('My app', 'http://localhost:3333')"
            if (s.includes('cf.studio')) {
                const match = s.match(`studio\\((\\s?)+(app=)?[\\'\\"](.*)[\\'\\"]\\,(\\s?)+(url=)?[\\'\\"](.*?)[\\'\\"]\\)`);
                if (match) {
                    iframeUrl = match[6];
                    if (iframeUrl && iframeUrl.startsWith('http')) {
                        iframeUrl = iframeUrl.trim();
                        // Adding trailing slash if missing
                        iframeUrl = iframeUrl.replace(/\/?$/, '/');
                    }
                } else {
                    iframeUrl = 'https://chartfactor.com/studio/';
                }
            }
        });

        return iframeUrl;
    }

    /**
     * This function send the Charfactor Studio info contained in the cell's metadata
     * to chartfactor.com/studio to save it into the local storage.
     * @param {} cell 
     */
    sendCfsInfoToStudio(cell) {
        this.createTempIframe(this.getIframeUrl(cell), cell, this.sendPostMessageToStudio);
    }

    /**
     * Sends the cell's app to studio local storage
     * @param {*} notebookConfig 
     */
    synchronizeNotebook(notebookConfig) {
        // Synchronizing the apps and the providers with CF Studio
        for (const cell of notebookConfig.cells) {
            if (cell.cell_type === 'code' && get(cell.metadata, 'cf_studio_app')) {
                this.sendCfsInfoToStudio(cell);
                this.setGlobalActiveCellId(cell.id);
            }
        }
    }

    /**
     * Gets the current notebook model configuration
     * @returns 
     */
    getNotebookConfig() {
        const current = getCurrent(null, this.app, this.notebook);
        const notebookConfig = current.model.toJSON(current.model);

        return notebookConfig;
    }

    /**
     * Remove the app from studio local storage
     * @param {*} cell 
     */
    removeFromLocalStorage(cell) {
        StorageUtils.remove(`cfs.app-${cell.id}`);
        const sendRemoveMessage = (cell, cellIFrame) => {
            cellIFrame.contentWindow.postMessage({
                action: 'removeStudioApp',
                storageKey: `cfs.app-${cell.id}`
            }, '*');
            setTimeout(() => {
                document.body.removeChild(cellIFrame);
            }, 1);
        }
        this.createTempIframe(this.getIframeUrl(cell), cell, sendRemoveMessage);
    }

    createNew(panel, context) {
        try {
            window.removeEventListener('message', window.cfsJlabSynchronizeMessageEventListener, false);
        } catch (e) { }
        window.addEventListener('message', window.cfsJlabSynchronizeMessageEventListener = this.cfsJlabSynchronizeMessageEventListener, false);

        /**
         * When the promise is fullfilled, then every 'code' cell is being checking 
         * in order to detect if contains any ChartFactor Studio app in the metadata,
         * and send that info to Studio to save it in the local storage.
         */
        context.sessionContext.ready.then(async () => {
            this.kernel = context.sessionContext.session.kernel;
            this.kernel.connectionStatusChanged.connect((kernel, status) => {
                if (status === 'disconnected') {
                    let notebookConfig = context.model.toJSON(context.model);

                    for (const cell of notebookConfig.cells) {
                        if (cell.cell_type === 'code' && get(cell.metadata, 'cf_studio_app')) {
                            try {
                                this.removeFromLocalStorage(cell);
                            } catch (error) {
                                this.removeFromLocalStorage(cell);
                            }
                        }
                    }
                }
            });

            this.synchronizeNotebook(this.getNotebookConfig());
        }).catch(e => console.error(e))

        NotebookActions.executionScheduled.connect(async (_, args) => {
            const { cell } = args;

            this.setGlobalActiveCellId(cell.model.id);
        });

        context.saveState.connect(this.onSave, this);
        this.notebook.activeCellChanged.connect(this.onActiveCellChanged, this);

        return new DisposableDelegate(() => {
            return;
        });
    }
}
