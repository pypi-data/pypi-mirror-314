export class KernelModel {
  constructor(session) {
    this._sessionContext = session;
    this._future = null;
    this._kernel_id = undefined;
  }

  future(value, resolve = null) {
    this._future = value;
    if (!value) {
      return;
    }

    value.onIOPub = (msg) => {
      const msgType = msg.header.msg_type;

      switch (msgType) {
        case 'execute_result':
          if (resolve) {
            const data = msg.content.data['text/plain'] || '';
            resolve(data);
          } else {
            resolve('');
          }                   
          break;
        case 'display_data':
          if (resolve) {
            resolve('');
          }
          break;
        case 'update_display_data':
          if (resolve) {
            resolve('');
          }
          break;
        case 'stream':
          if (resolve) {
            resolve(msg.content.text.trim());
          } else {
            resolve('');
          }          
          break;
        case 'error':
          if(resolve && msg.content.ename && msg.content.evalue) {      
            if (msg.content.evalue === "name 'cf' is not defined") {
              msg.content.evalue = "Name 'cf' is not defined. Please execute 'from chartfactor import *' in any cell above.";
            }                      
            resolve(`{"ename": "${msg.content.ename}", "evalue": "${msg.content.evalue}"}`);
          } else {
            resolve('');
          }         
          break;
        default:
          break;
      }
      return;
    };
  }

  execute(code, resolve = null) {
    if (!this._sessionContext || !this._sessionContext.session?.kernel) {
      resolve('{"ename": "KernelOff", "evalue": "It appears that the Jupyter Lab Kernel of this notebook has changed since the last run. Please import chartactor and run the cell again."}');
    }

    this.future(this._sessionContext.session?.kernel?.requestExecute({
      code
    }), resolve);
  }
}
