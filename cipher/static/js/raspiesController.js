/* globals socket */
/* globals alert */

/* exported raspiesController */
const raspiesController = (() => {
  'use strict';

  let connected_raspies = [];
  let on_connect_listeners = [];
  let on_disconnect_listeners = [];

  /* PUBLIC METHODS */
  function init() {
    bindUIEvents();
    bindSocketIOEvents();
    socket.emit('get_raspies');
  }

  /* PRIVATE METHODS */
  function bindUIEvents(){
  }

  function bindSocketIOEvents() {
    socket.on('raspi_disconnect', (raspi) => {
      connected_raspies = connected_raspies.filter(r => r.id != raspi.id);
      raspiDisconnectAlert(raspi.id);
      on_disconnect_listeners.forEach(l => l(raspi));
    });

    socket.on('raspi_connect', (raspi) => {
      connected_raspies = connected_raspies.filter(r => r.id != raspi.id); // first delete the raspi with the same id (if it exists)
      connected_raspies.push(raspi);
      raspiConnectAlert(raspi.id);
      on_connect_listeners.forEach(l => l(raspi));
    });

    socket.on('receive_raspies', (raspies) => {
      connected_raspies = raspies;
      if(raspies.length > 0)
        on_connect_listeners.forEach(l => raspies.forEach(r => l(r)));
    });
  }

  function raspiConnectAlert(raspi_id) {
    alert('<i class=\'fab fa-raspberry-pi\'></i> Raspberry connecté !', 
      'Le raspberry <strong>' + raspi_id + '</strong> s\'est connecté.',
      'orange');
  }

  function raspiDisconnectAlert(raspi_id) {
    alert('<i class=\'fab fa-raspberry-pi\'></i> Raspberry déconnecté !', 
      'Le raspberry <strong>' + raspi_id + '</strong> s\'est déconnecté.',
      'orange');
  }

  function addOnConnectListener(callback) {
    on_connect_listeners.push(callback);
  }

  function addOnDisconnectListener(callback) {
    on_disconnect_listeners.push(callback);
  }

  function getRaspies() {
    return connected_raspies;
  }

  return {
    init: init,
    addOnConnectListener: addOnConnectListener,
    addOnDisconnectListener: addOnDisconnectListener,
    getRaspies: getRaspies
  };
})();
