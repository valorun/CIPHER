/* globals socket */
/* globals clientsController */

/* exported clientsManagementController */
const clientsManagementController = (() => {
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
    document.getElementById('shutdown-button').addEventListener('click', () => {
      socket.emit('shutdown');
    });
    document.getElementById('reboot-button').addEventListener('click', () => {
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
    const card = '<div id=\'' + client.id + '-card\' class=\'client-card\'>' +
    '<header><i class=\'' + client.icon + '\'></i></header>' +
    '<span>' + client.id + '</span>' +
    '</div>';
    DOM.$clients.insertAdjacentHTML('beforeend', card);
  }

  function removeClientCard(client) {
    const el = document.getElementById(client.id + '-card');
    if (el != null) {
      el.parentNode.removeChild(el);
    }
  }

  return {
    init: init
  };
})();
