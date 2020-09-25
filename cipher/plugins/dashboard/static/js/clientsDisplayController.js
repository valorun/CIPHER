/* globals socket */
/* globals clientsController */

/* exported clientsDisplayController */
const clientsDisplayController = (() => {
  'use strict';
  const DOM = {};

  /* PUBLIC METHODS */
  function init() {
    cacheDom();
    bindUIEvents();
    bindSocketIOEvents();
  }

  /* PRIVATE METHODS */
  function bindUIEvents() {
    document.getElementById('shutdownButton').addEventListener('click', () => {
      socket.emit('shutdown');
    });
    document.getElementById('rebootButton').addEventListener('click', () => {
      socket.emit('reboot');
    });
  }

  function bindSocketIOEvents() {
    clientsController.addOnConnectListener((c) => addClientCard(c));
    clientsController.addOnDisconnectListener((c) => removeClientCard(c));
  }

  function cacheDom() {
    DOM.$clients = document.getElementById('clients');
  }

  function addClientCard(client) {
    // first delete the already existing card for the client (if it exists) ...
    removeClientCard(client);
    const card = '<div id=\'' + client.id + '_card\' class=\'container cell center pale-green round-large border border-green padding-16\'' +
    '<h3><strong><i class=\'xxxlarge ' + client.icon + '\'></i></strong></h3>' +
    '<h3>' + client.id + '</h3>' +
    '</div>';
    DOM.$clients.insertAdjacentHTML('beforeend', card);
  }

  function removeClientCard(client) {
    const el = document.getElementById(client.id + '_card');
    if (el != null) {
      el.parentNode.removeChild(el);
    }
  }

  return {
    init: init
  };
})();
