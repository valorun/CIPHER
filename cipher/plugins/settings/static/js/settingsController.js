/* globals successAlert */
/* globals fetchJson */
/* globals empty */
/* globals clientsController */

/* exported settingsController */
const settingsController = (() => {
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
    // audio on server mode
    document.getElementById('audioOnServer').addEventListener('change', (e) => {
      fetchJson('/update_audio_source', 'POST', { value: e.srcElement.checked })
        .then(r => successAlert(r));
    });

    // motion raspi id modification
    document.getElementById('motionRaspiIdForm').addEventListener('submit', (e) => {
      e.preventDefault();
      fetchJson('/update_motion_raspi_id', 'POST', { raspi_id: DOM.$motionRaspiId.value })
        .then(r => successAlert(r));
    });

    // enable motion
    document.getElementById('enableMotion').addEventListener('change', (e) => {
      fetchJson('/update_enable_motion', 'POST', { value: e.srcElement.checked })
        .then(r => successAlert(r));
    });

    // robot name modification
    document.getElementById('robotNameForm').addEventListener('submit', (e) => {
      e.preventDefault();
      fetchJson('/update_robot_name', 'POST', { robot_name: DOM.$robotName.value })
        .then(r => successAlert(r));
    });
  }
  function bindSocketIOEvents() {
    // clients autocompletes
    clientsController.addOnConnectListener((c) => {
      DOM.$availableRaspies.insertAdjacentHTML('beforeend', '<option id="' + c.id + '_client" value="' + c.id + '">');
    });
    clientsController.addOnDisconnectListener((c) => {
      const $el = document.getElementById(c.id + '_client');
      if ($el != null) {
        $el.parentNode.removeChild($el);
      }
    });
  }

  function cacheDom() {
    DOM.$robotName = document.getElementById('robotName');
    DOM.$motionRaspiId = document.getElementById('motionRaspiId');
    DOM.$availableRaspies = document.getElementById('availableRaspies');
  }

  return {
    init: init
  };
})();
