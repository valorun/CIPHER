/* globals fetchJson */
/* globals successAlert */

/* exported relaysSettingsController */
const relaysSettingsController = (() => {
  'use strict';

  const DOM = {};

  /* PUBLIC METHODS */
  function init() {
    cacheDom();
    bindUIEvents();
  }

  /* PRIVATE METHODS */
  function bindUIEvents() {
    document.getElementById('addRelay').addEventListener('click', () => {
      fetchJson('/save_relay', 'POST',
        {
          rel_label: DOM.$newRelayLabel.value,
          rel_pin: DOM.$newRelayPin.value,
          rel_parity: DOM.$newRelayParity.value,
          raspi_id: DOM.$newRelayRaspiId.value
        })
        .then(() => {
          location.reload();
        });
    });

    // checkbox to enable or disable the relay
    document.querySelectorAll('input[name=enableRel]').forEach(e => {
      const relLabel = e.id.substring(e.id.indexOf('_') + 1);
      e.addEventListener('change', () => {
        enableRelay(relLabel, e.checked);
      });
    });

    // button to delete the relay
    document.querySelectorAll('a[name=deleteRel]').forEach(e => {
      const relLabel = e.id.substring(e.id.indexOf('_') + 1);
      e.addEventListener('click', () => {
        deleteRelay(relLabel);
      });
    });
  }

  function cacheDom() {
    DOM.$newRelayLabel = document.getElementById('newRelayLabel');
    DOM.$newRelayPin = document.getElementById('newRelayPin');
    DOM.$newRelayParity = document.getElementById('newRelayParity');
    DOM.$newRelayRaspiId = document.getElementById('newRelayRaspiId');
  }

  /**
  * Enable OR disable a relay
  * @param {string} relLabel relay label
  * @param {boolean} value new state for the relay
  */
  function enableRelay(relLabel, value) {
    fetchJson('/enable_relay', 'POST', { rel_label: relLabel, value: value })
      .then((r) => {
        successAlert(r);
        console.log(relLabel + ' updated');
      });
  }

  /**
  * Delete a relay
  * @param {string} rel_label relay label
  */
  function deleteRelay(relLabel) {
    const confirm = window.confirm('Etes vous sûr de vouloir supprimer le relai \'' + relLabel + '\' ?');
    if (confirm) {
      fetchJson('/delete_relay', 'POST', { rel_label: relLabel })
        .then((r) => {
          successAlert(r);
          console.log(relLabel + ' deleted');
          const el = document.getElementById(relLabel);
          el.parentNode.removeChild(el);
        });
    }
  }

  return {
    init: init
  };
})();
