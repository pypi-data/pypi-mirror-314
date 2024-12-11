window.executePython = function (python, kernelId, action = undefined, df = '', config = '') {
    if (typeof Jupyter !== 'undefined') {
        return new Promise((resolve, reject) => {
            var callback = {
                iopub: {
                    output: (data) => {
                        if (data.content.text) {
                            resolve(data.content.text.trim());
                        } else if (data.content.ename && data.content.evalue) {
                            if (data.content.evalue === "name 'cf' is not defined") {
                                data.content.evalue = "Name 'cf' is not defined. Please execute 'from chartfactor import *' in any cell above.";
                            }
                            resolve(`{"ename": "${data.content.ename}", "evalue": "${data.content.evalue}"}`);
                        } else {
                            resolve('');
                        }
                    }
                }
            };

            Jupyter.notebook.kernel.execute(`${python}`, callback);
        });
    } else if (typeof JupyterLab !== 'undefined' || typeof jupyterlab !== 'undefined') {
        return new Promise((resolve, reject) => {
            if (typeof JupyterLab !== 'undefined' && JupyterLab[kernelId]) { // Running on JupyterLab environment
                JupyterLab[kernelId].notebook.kernel.execute(`${python}`, resolve);
            } else if (
                (typeof JupyterLab !== 'undefined' && JupyterLab.context?.sessionContext.session?.kernel) ||
                (typeof jupyterlab !== 'undefined' && jupyterlab.shell.currentWidget?.context?.sessionContext.session?.kernel)
            ) { // Running on Kaggle or any other environment that supports JupyterLab
                const future = (value) => {
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
                                if (resolve && msg.content.ename && msg.content.evalue) {
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

                const code = `${python}`;
                if (typeof JupyterLab !== 'undefined') {
                    future(JupyterLab.context.sessionContext.session?.kernel.requestExecute({ code }));
                } else {
                    const onActiveCellChanged = function onActiveCellChanged(event) {
                        if (event.activeCell) {
                            this.setGlobalActiveCellId(event.activeCell.model.id);
                        }
                    }
                    future(jupyterlab.shell.currentWidget.context.sessionContext.session.kernel.requestExecute({code}));
                }

            } else {
                resolve(`{"ename": "Kernel", "evalue": "It appears that the Jupyter Lab Kernel of this notebook has changed since the last run. Please import chartactor and run the cell again."}`);
            }
        });
    } else if (typeof google !== 'undefined' && google.colab) {
        return new Promise((resolve, reject) => {
            const processOutput = (response) => {
                if (response.ename && response.evalue) {
                    if (response.evalue === "name 'cf' is not defined") {
                        response.evalue = "Name 'cf' is not defined. Please execute 'from chartfactor import *' in any cell above.";
                    }
                    resolve(`{"ename": "${response.ename}", "evalue": "${response.evalue}"}`);
                } else if (response.data['text/plain']) {
                    resolve(response.data['text/plain'].trim().slice(1, -1).replace(/\\'/g, "'").replace(/\\\\/g, "\\"));
                } else {
                    resolve('');
                }
            }

            switch (action) {
                case "getDatasources":
                    google.colab.kernel.invokeFunction("get_data_sources", [], {}).then(response => processOutput(response));
                    break;
                case "getDatasource":
                    google.colab.kernel.invokeFunction("get_data_source", [df], {}).then(response => processOutput(response));
                    break;
                case "runCountQuery":
                    google.colab.kernel.invokeFunction("run_count_query", [df, JSON.stringify(config)], {}).then(response => processOutput(response));
                    break;
                case "runRawQuery":
                    google.colab.kernel.invokeFunction("run_raw_query", [df, JSON.stringify(config)], {}).then(response => processOutput(response));
                    break;
                case "visualize":
                    google.colab.kernel.invokeFunction("visualize", [df, JSON.stringify(config)], {}).then(response => processOutput(response));
                    break;
                default:
                    break;
            }
        });
    }
}
