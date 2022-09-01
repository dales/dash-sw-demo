setTimeout(()=> {
dragula([document.getElementById('view-list')], {
                direction: 'verticle',
                moves: function (el, container, handle) {
                    return handle.classList.contains('drag-handle');
                }
            })
}, 1000)
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        image_cache: {},
        dragging_setup: (plugins) => {


            return dash_clientside.no_update
        },
    }
})
