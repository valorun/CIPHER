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
  }

  function bindSocketIOEvents() {
    clientsController.addOnConnectListener((c) => addClientTag(c));
    clientsController.addOnDisconnectListener((c) => removeClientTag(c));
  }

  function cacheDom() {
    DOM.$clients = document.getElementById('clients-bar');
  }

  function addClientTag(client) {
    // first delete the already existing tag for the client (if it exists) ...
    removeClientTag(client);
    const tag = '<div id=\'' + client.id + '-tag\' class=\'client-tag\'>' +
    '<header><i class=\'' + client.icon + '\'></i></header>' +
    '<span>' + client.id + '</span>' +
    '</div>';
    DOM.$clients.insertAdjacentHTML('beforeend', tag);
  }

  function removeClientTag(client) {
    const el = document.getElementById(client.id + '-tag');
    if (el != null) {
      el.parentNode.removeChild(el);
    }
  }

  return {
    init: init
  };
})();
