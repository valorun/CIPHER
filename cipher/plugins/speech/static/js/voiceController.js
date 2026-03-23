/* globals fetchJson */
/* globals successAlert */
/* globals failAlert */
/* globals socket */

/* exported voiceController */
const voiceController = (() => {
  'use strict';

  const DOM = {};

  const TEST_SENTENCE = "Bonjour, j'espère que ma voix vous convient !";

  /* PUBLIC METHODS */
  function init() {
    cacheDom();
    bindUIEvents();
  }

  /* PRIVATE METHODS */
  function bindUIEvents() {
    DOM.$saveVoiceButton.addEventListener('click', () => {
        fetchJson('/save_voice', 'POST',
          {
            voice_name: DOM.$voiceName.value
          })
          .then((r) => {
            successAlert(r);
          }).catch((err) => {
            failAlert('Une erreur est survenue.');
          });
    });

    DOM.$testVoiceButton.addEventListener('click', () => {
      socket.emit('action', 'speech', { text: TEST_SENTENCE });
    });
  }

  function cacheDom() {
    DOM.$voiceName = document.getElementById('voice-name');
    DOM.$saveVoiceButton = document.getElementById('save-voice-button');
    DOM.$testVoiceButton = document.getElementById('test-voice-button');
  }

  return {
    init: init
  };
})();
