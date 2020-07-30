/* globals Cookies */
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
    window.speechSynthesis.onvoiceschanged = this.fillVoices;
    cacheDom();
    bindUIEvents();
    fillVoices();
    socket.emit('get_raspies');
  }

  /* PRIVATE METHODS */
  function bindUIEvents() {
    // voice selection
    DOM.$voices.addEventListener('change', () => {
      Cookies.set('voice', DOM.$voices.value);
    });

    // raspies autocompletes
    socket.on('receive_raspies', (raspies) => {
      raspies = raspies.map(r => r.id);
      document.querySelectorAll('#newRelayRaspiIdData,#newServoRaspiIdData,#motionRaspiIdData').forEach((e) => {
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
    DOM.$voices = document.getElementById('voices');
    DOM.$robotName = document.getElementById('robotName');
    DOM.$motionRaspiId = document.getElementById('motionRaspiId');
  }

  function fillVoices() {
    const voices = window.speechSynthesis.getVoices();
    empty(DOM.$voices);

    voices.forEach((e) => {
      if (typeof Cookies.get('voice') !== 'undefined' &&
      Cookies.get('voice') === e.name) { // if a voice has already been chosen, select it
        DOM.$voices.insertAdjacentHTML('beforeend', '<option selected=\'selected\' value=' + e.name + '>' +
        e.name + '</option>');
      } else {
        DOM.$voices.insertAdjacentHTML('beforeend', '<option value=' + e.name + '>' +
        e.name + '</option>');
      }
    });
  }

  return {
    init: init
  };
})();
