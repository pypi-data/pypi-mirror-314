window.sendMessage = function (r, fId, a, reqId) {
    try {
        JSON.parse(r);
    } catch (e) {
        console.log(r);
        r = '{"data": {"data": [], "visualization": ""}}'
    }

    const iframe = document.getElementById(fId)
    if (iframe) {
        iframe.contentWindow.postMessage({ response: r, action: a, reqId }, '*');
    }
};
