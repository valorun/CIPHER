/* globals fetchJson */
/* globals successAlert */
/* globals failAlert */
/* globals socket */

/* exported voiceController */
const voiceController = (() => {
  'use strict';

  const DOM = {};

  let effectsEntries = [];

  const TEST_SENTENCE = 'Bonjour, ma voix vous convient-elle ?';

  class VoiceEffectEntry {
    constructor($tr) {
      this.$tr = $tr;
      this.name = $tr.dataset.name;
      this.$value = $tr.getElementsByClassName('effect-value')[0];
      this.$enabled = $tr.getElementsByClassName('effect-enabled')[0];
    }

    get value() {
      return parseInt(this.$value.value);
    }

    get enabled() {
      return this.$enabled.checked;
    }

    toJSON() {
      return {
        name: this.name,
        enabled: this.enabled,
        value: this.value
      };
    }
  }
  /* PUBLIC METHODS */
  function init() {
    cacheDom();
    bindUIEvents();
  }

  /* PRIVATE METHODS */
  function bindUIEvents() {
    DOM.$saveVoiceButton.addEventListener('click', () => {
      if (effectsEntries.every(e => e.$value.checkValidity())) {
        fetchJson('/save_voice', 'POST',
          {
            voice_name: DOM.$voiceName.value,
            effects: effectsEntries.map(e => e.toJSON())
          })
          .then((r) => {
            successAlert(r);
          });
      } else {
        failAlert('Une ou plusieurs valeurs renseignées sont incorrectes.');
      }
    });

    DOM.$testVoiceButton.addEventListener('click', () => {
      socket.emit('action', 'speech', { text: TEST_SENTENCE });
    });
  }

  function cacheDom() {
    DOM.$voiceName = document.getElementById('voiceName');
    DOM.$saveVoiceButton = document.getElementById('saveVoiceButton');
    DOM.$testVoiceButton = document.getElementById('testVoiceButton');
    effectsEntries = Array.from(document.getElementById('effects_table').rows).slice(1).map(element => new VoiceEffectEntry(element));
  }

  return {
    init: init
  };
})();
