/* globals fetchJson */
/* globals successAlert */

/* exported relaysSettingsController */
const relaysSettingsController = (() => {
  'use strict';

  const DOM = {};

  let relaysEntries = [];

  class RelayEntry {
    constructor($tr) {
      this.$tr = $tr;
      this.label = $tr.dataset.label;
      this.$label = $tr.getElementsByClassName('relay-label')[0];
      this.$pin = $tr.getElementsByClassName('relay-pin')[0];
      this.$parity = $tr.getElementsByClassName('relay-parity')[0];
      this.$raspi = $tr.getElementsByClassName('relay-raspi')[0];

      this.$delete = $tr.getElementsByClassName('relay-delete')[0];
      this.$save = $tr.getElementsByClassName('relay-save')[0];
      this.$enable = $tr.getElementsByClassName('relay-enable')[0];

      this.$save.addEventListener('click', () => this.update());
      this.$enable.addEventListener('click', () => this.enable(this.$enable.checked));
      this.$delete.addEventListener('click', () => this.delete());

      this.onDestroyCallback = null;
    }

    /**
     * Sends the new servo data to the server and updates it
     */
    update() {
      fetchJson('/update_relay', 'POST', {
        label: this.label,
        new_label: this.$label.value,
        pin: this.$pin.value,
        parity: this.$parity.value,
        raspi_id: this.$raspi.value
      }).then((r) => {
        successAlert(r);
        console.log(this.label + ' updated');
        this.label = this.$label.value;
        this.$tr.dataset.label = this.label;
      });
    }

    /**
     * Delete the relay
     */
    delete() {
      const confirm = window.confirm('Etes vous sûr de vouloir supprimer le relai \'' + this.label + '\' ?');
      if (confirm) {
        fetchJson('/delete_relay', 'POST', { label: this.label })
          .then((r) => {
            successAlert(r);
            console.log('Relay \'' + this.label + '\' deleted');
            this.$tr.parentNode.removeChild(this.$tr);
            if (this.onDestroyCallback !== null) {
              this.onDestroyCallback();
            }
          });
      }
    }

    /**
    * Enable OR disable the relay
    * @param {boolean} value new state for the relay
    */
    enable(value) {
      fetchJson('/enable_relay', 'POST', { label: this.label, value: value })
        .then((r) => {
          successAlert(r);
          console.log(this.label + ' updated');
        });
    }

    /**
     * Add a callback executed when the servo table element is deleted.
     * @param {*} func callback function
     */
    onDestroy(func) {
      this.onDestroyCallback = func;
    }
  }
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
          label: DOM.$newRelayLabel.value,
          pin: DOM.$newRelayPin.value,
          parity: DOM.$newRelayParity.value,
          raspi_id: DOM.$newRelayRaspiId.value
        })
        .then(() => {
          location.reload();
        });
    });
  }

  function cacheDom() {
    DOM.$newRelayLabel = document.getElementById('newRelayLabel');
    DOM.$newRelayPin = document.getElementById('newRelayPin');
    DOM.$newRelayParity = document.getElementById('newRelayParity');
    DOM.$newRelayRaspiId = document.getElementById('newRelayRaspiId');

    relaysEntries = Array.from(document.getElementById('relays_table').rows).slice(1).map(element => new RelayEntry(element));
    // remove relay entry from list when its element is deleted
    relaysEntries.forEach(e => e.onDestroy(s => {
      relaysEntries = relaysEntries.filter(s1 => s1.label !== e.label);
    }));
  }

  return {
    init: init
  };
})();
