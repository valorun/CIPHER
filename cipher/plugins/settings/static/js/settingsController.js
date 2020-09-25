/* globals socket */
/* globals successAlert */
/* globals fetchJson */
/* globals empty */

/* exported settingsController */
const settingsController = (() => {
  'use strict';

  const DOM = {};

  /* PUBLIC METHODS */
  function init() {
    cacheDom();
    bindUIEvents();
    socket.emit('get_raspies');
  }

  /* PRIVATE METHODS */
  function bindUIEvents() {
    // raspies autocompletes
    socket.on('receive_raspies', (raspies) => {
      raspies = raspies.map(r => r.id);
      document.querySelectorAll('#availableRaspies').forEach((e) => {
        empty(e);
        raspies.forEach((r) => {
          e.insertAdjacentHTML('beforeend', '<option value="' + r + '">');
        });
      });
    });

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

  function cacheDom() {
    DOM.$robotName = document.getElementById('robotName');
    DOM.$motionRaspiId = document.getElementById('motionRaspiId');
  }

  return {
    init: init
  };
})();
