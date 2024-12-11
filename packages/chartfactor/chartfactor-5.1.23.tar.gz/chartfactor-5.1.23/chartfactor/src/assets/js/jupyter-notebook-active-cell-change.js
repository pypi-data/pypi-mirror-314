window.onActiveCellChanged = function (event, data) {            
    const { cell } = data;
    Jupyter.notebook.kernel.execute(`cfpy_active_cell_id = '${cell.id}'`, {}, {silent: true});
};

(() => {
    if (typeof Jupyter !== 'undefined') {
        Jupyter.notebook.events.off('select.Cell', window.onActiveCellChanged);
        Jupyter.notebook.events.on('select.Cell', window.onActiveCellChanged);
    }
})()
