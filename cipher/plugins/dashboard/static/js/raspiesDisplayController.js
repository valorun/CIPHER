/* globals socket */
/* globals raspiesController */

/* exported raspiesDisplayController */
const raspiesDisplayController = (() => {
    'use strict';
    const DOM = {};

    /* PUBLIC METHODS */
    function init() {
        cacheDom();
        bindUIEvents();
        bindSocketIOEvents();
    }

    /* PRIVATE METHODS */
    function bindUIEvents(){
        document.getElementById('shutdownButton').addEventListener('click', () => {
            socket.emit('shutdown');
        });
        document.getElementById('rebootButton').addEventListener('click', () => {
            socket.emit('reboot');
        });
    }

    function bindSocketIOEvents() {
        raspiesController.addOnConnectListener((r) => addRaspiCard(r));
        raspiesController.addOnDisconnectListener((r) => removeRaspiCard(r));
    }

    function cacheDom() {
        DOM.$raspberries = document.getElementById('raspberries');
    }

    function addRaspiCard(raspi) {
        // first delete the already existing card for the raspi (if it exists) ...
        removeRaspiCard(raspi);
        const card = '<div id=\'' + raspi.id + '_card\' class=\'container cell center pale-green round-large border border-green padding-16\''+
                            '<h3><strong><i class=\'xxxlarge fab fa-raspberry-pi\'></i></strong></h3>' +
                            '<h3>' + raspi.id + '</h3>' +
                        '</div>';
        DOM.$raspberries.insertAdjacentHTML('beforeend', card);
    }

    function removeRaspiCard(raspi) {
        const el = document.getElementById(raspi.id + '_card');
        if(el != null)
            el.parentNode.removeChild(el);
    }

    return {
        init: init
    };
})();
