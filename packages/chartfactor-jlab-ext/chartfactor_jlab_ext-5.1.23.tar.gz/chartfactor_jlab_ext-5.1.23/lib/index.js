import { INotebookTracker } from '@jupyterlab/notebook';

import {
  ICommandPalette
} from '@jupyterlab/apputils';

import {
  IRenderMimeRegistry,
} from '@jupyterlab/rendermime';

const RunnerExtension = require('./runner').default;
const CfsExtension = require('./cfs').default;

const extension = [
  {
    id: 'chartfactor_jlab_ext',
    autoStart: true,
    requires: [INotebookTracker, ICommandPalette, IRenderMimeRegistry],
    activate: function (app, notebook, palette, mime) {
      console.log('JupyterLab extension chartfactor_jlab_ext is activated!');
      /**
       * Activate the extensions.
       */
      const runner = new RunnerExtension();
      const cfs = new CfsExtension(app, notebook);
      app.docRegistry.addWidgetExtension('Notebook', runner);
      app.docRegistry.addWidgetExtension('Notebook', cfs);
    }
  }
];

export default extension;
