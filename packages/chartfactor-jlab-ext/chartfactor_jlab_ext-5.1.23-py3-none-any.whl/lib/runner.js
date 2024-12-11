import { DisposableDelegate } from '@phosphor/disposable';
import { KernelModel } from './model';

export default class RunnerExtension {
    createNew(panel, context) {            
        const kernelModel = new KernelModel(context.sessionContext);        
        context.sessionContext.ready.then(s => {     
            kernelModel._kernel_id = context.sessionContext.session?.kernel?.id;                         

            if (!window.JupyterLab) {
                window.JupyterLab = {};
            }
            
            window.JupyterLab[kernelModel._kernel_id] = {
                notebook: {
                    kernel: kernelModel
                }
            };

        }).catch(e => console.error(e))                

        return new DisposableDelegate(() => {
            return;
        });
    }
}
