/* globals socket */
/* globals alert */

/* exported clientsController */
const clientsController = (() => {
  'use strict';

  let connectedClients = [];
  let onConnectListeners = [];
  let onDisconnectListeners = [];

  /* PUBLIC METHODS */
  function init() {
    bindUIEvents();
    bindSocketIOEvents();
    socket.emit('get_clients');
  }

  /* PRIVATE METHODS */
  function bindUIEvents() {
  }

  function bindSocketIOEvents() {
    socket.on('client_disconnect', (client) => {
      connectedClients = connectedClients.filter(r => r.id != client.id);
      clientDisconnectAlert(client.id, client.icon);
      onDisconnectListeners.forEach(l => l(client));
    });

    socket.on('client_connect', (client) => {
      connectedClients = connectedClients.filter(r => r.id != client.id); // first delete the raspi with the same id (if it exists)
      connectedClients.push(client);
      clientConnectAlert(client.id, client.icon);
      onConnectListeners.forEach(l => l(client));
    });

    socket.on('receive_clients', (clients) => {
      connectedClients = clients;
      if (clients.length > 0) {
        onConnectListeners.forEach(l => clients.forEach(r => l(r)));
      }
    });
  }

  function clientConnectAlert(clientId, clientIcon) {
    alert('<i class=\'' + clientIcon + '\'></i> Client connecté !',
      'Le client <strong>' + clientId + '</strong> s\'est connecté.',
      'orange');
  }

  function clientDisconnectAlert(clientId, clientIcon) {
    alert('<i class=\'' + clientIcon + '\'></i> Client déconnecté !',
      'Le client <strong>' + clientId + '</strong> s\'est déconnecté.',
      'orange');
  }

  function addOnConnectListener(callback) {
    onConnectListeners.push(callback);
  }

  function addOnDisconnectListener(callback) {
    onDisconnectListeners.push(callback);
  }

  function getClients() {
    return connectedClients;
  }

  return {
    init: init,
    addOnConnectListener: addOnConnectListener,
    addOnDisconnectListener: addOnDisconnectListener,
    getClients: getClients
  };
})();
