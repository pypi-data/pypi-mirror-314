import { StorageUtils, getProvidersFromApp } from './storage-utils';
import { uniqBy, has } from 'lodash';
import { INotification } from 'jupyterlab_toastify';
/**
 * Function to get the current notebook including the ipynb content
 * @param {*} args 
 * @returns current active notebook
 */
export const getCurrent = (args = null, app, notebooks) => {
    const widget = notebooks.currentWidget;
    const activate = args ? args['activate'] !== false : false;

    if (activate && widget) {
        app.shell.activateById(widget.id);
    }

    return widget;
}

export const toJSONWithDasboards = (json) => {
    return () => {
        let success = false;

        json.cells.forEach((cell) => {
            if (cell.cell_type === 'code') {
                const app = StorageUtils.get(`cfs.app-${cell.id}`);

                if (app) {
                    const appProviders = getProvidersFromApp(app);

                    if (!has(cell['metadata'], 'cf_studio_app')) {
                        cell['metadata']['cf_studio_app'] = {};
                    }

                    if (!has(cell['metadata'], 'cf_studio_providers')) {
                        cell['metadata']['cf_studio_providers'] = [];
                    }

                    cell['metadata']['cf_studio_app'][`cfs.app-${cell.id}`] = app;
                    cell['metadata']['cf_studio_providers'] = uniqBy([...appProviders], 'name');

                    success = true;
                }
            }
        });

        if (success && window.souldDisplaySaveMessage) {
            INotification.success('The cf.studio apps were saved into this notebook');
        }

        return json;
    }
};
