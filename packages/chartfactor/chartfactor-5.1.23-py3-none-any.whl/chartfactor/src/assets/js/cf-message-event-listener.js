function cfMessageEventListener (event) {
    let python_code = "";

    if (event.data.action === 'getDatasources') {
        python_code = "print(json.dumps([{'id': g, 'name': g, 'providerType': 'pandas-dataframe', 'type': 'DATASET' } for g in globals() if isinstance(eval(g), pd.core.frame.DataFrame)]))";
    } else if (event.data.action === 'getDatasource') {
        python_code = `print(cf.provider(${event.data.df}).get_data_source('${event.data.df}'))`
    } else if (event.data.action === 'visualize') {
        python_code = `print(cf.provider(${event.data.df}, json.loads('''${JSON.stringify(event.data.conf)}''')).visualize())`
    } else if (event.data.action === 'runCountQuery') {
        python_code = `print(cf.provider(${event.data.df}, json.loads('''${JSON.stringify(event.data.conf)}''')).run_count_query())`
    } else if (event.data.action === 'runRawQuery') {
        python_code = `print(cf.provider(${event.data.df}, json.loads('''${JSON.stringify(event.data.conf)}''')).run_raw_query())`
    } else if (event.data.action === 'isLoadedInJupyter') {
        const iframe = document.getElementById(event.data.iframe)
        if (iframe) {
            iframe.contentWindow.postMessage({ response: 'OK', action: event.data.action, reqId: event.data.reqId }, '*');
        }
    } else if (event.data.action === 'resizeIframeHeight') {
        document.getElementById(event.data.iframe).style.setProperty('height', `${event.data.iframeHeight + 100}px`);
        if (typeof google !== 'undefined' && google.colab) {
            const height = event.data.iframeHeight + 130;
            google.colab.output.setIframeHeight(height, true, {
                maxHeight: height,
            });
        }
    }

    if (python_code !== "" && window.executePython) {
        let kernelId = event.data.iframe.split('_');
        if (kernelId && kernelId.length === 2) kernelId = kernelId[1];

        const promise = window.executePython(python_code, kernelId, event.data.action, event.data.df, event.data.conf);

        if (promise) {
            promise.then(result => {
                window.sendMessage(result, `${event.data.iframe}`, `${event.data.action}`, `${event.data.reqId}`);
            });
        }
    }
};

(() => {
    try{ window.removeEventListener('message', window.cfMessageEventListener, false); } catch(e) {}
    window.addEventListener('message', window.cfMessageEventListener = cfMessageEventListener, false);
})();