/* globals fetchJson */
/* globals successAlert */

/* exported servosSettingsController */
const servosSettingsController = (() => {
  'use strict';

  const DOM = {};

  let servosEntries = [];

  class ServoEntry {
    constructor($tr) {
      this.$tr = $tr;
      this.label = $tr.dataset.label;
      this.$label = $tr.getElementsByClassName('servo-label')[0];
      this.$pin = $tr.getElementsByClassName('servo-pin')[0];
      this.$min = $tr.getElementsByClassName('servo-min')[0];
      this.$max = $tr.getElementsByClassName('servo-max')[0];
      this.$default = $tr.getElementsByClassName('servo-default')[0];
      this.$raspi = $tr.getElementsByClassName('servo-raspi')[0];

      this.$delete = $tr.getElementsByClassName('servo-delete')[0];
      this.$save = $tr.getElementsByClassName('servo-save')[0];
      this.$enable = $tr.getElementsByClassName('servo-enable')[0];

      this.$save.addEventListener('click', () => this.update());
      this.$enable.addEventListener('click', () => this.enable(this.$enable.checked));
      this.$delete.addEventListener('click', () => this.delete());

      this.onDestroyCallback = null;
    }

    /**
     * Sends the new servo data to the server and updates it
     */
    update() {
      fetchJson('/update_servo', 'POST', {
        label: this.label,
        new_label: this.$label.value,
        pin: this.$pin.value,
        raspi_id: this.$raspi.value,
        min_pulse_width: this.$min.value,
        max_pulse_width: this.$max.value,
        def_pulse_width: this.$default.value
      }).then((r) => {
        successAlert(r);
        console.log(this.label + ' updated');
        this.label = this.$label.value;
        this.$tr.dataset.label = this.label;
      });
    }

    /**
     * Delete the servo
     */
    delete() {
      const confirm = window.confirm('Etes vous sûr de vouloir supprimer le servomoteur \'' + this.label + '\' ?');
      if (confirm) {
        fetchJson('/delete_servo', 'POST', { label: this.label })
          .then((r) => {
            successAlert(r);
            console.log('Servo \'' + this.label + '\' deleted');
            this.$tr.parentNode.removeChild(this.$tr);
            if (this.onDestroyCallback !== null) {
              this.onDestroyCallback();
            }
          });
      }
    }

    /**
    * Enable OR disable the servo
    * @param {boolean} value new state for the servo
    */
    enable(value) {
      fetchJson('/enable_servo', 'POST', { label: this.label, value: value })
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
    document.getElementById('addServo').addEventListener('click', () => {
      fetchJson('/save_servo', 'POST',
        {
          label: DOM.$newServoLabel.value,
          pin: DOM.$newServoPin.value,
          min_pulse_width: DOM.$newServoMinPulseWidth.value,
          max_pulse_width: DOM.$newServoMaxPulseWidth.value,
          def_pulse_width: DOM.$newServoDefPulseWidth.value,
          raspi_id: DOM.$newServoRaspiId.value
        }).then(() => {
        location.reload();
      });
    });
    servosEntries = Array.from(document.getElementById('servos_table').rows).slice(1).map(element => new ServoEntry(element));
    // remove servo entry from list when its element is deleted
    servosEntries.forEach(e => e.onDestroy(s => {
      servosEntries = servosEntries.filter(s1 => s1.label !== e.label);
    }));
  }

  function cacheDom() {
    DOM.$newServoLabel = document.getElementById('newServoLabel');
    DOM.$newServoPin = document.getElementById('newServoPin');
    DOM.$newServoMinPulseWidth = document.getElementById('newServoMinPulseWidth');
    DOM.$newServoMaxPulseWidth = document.getElementById('newServoMaxPulseWidth');
    DOM.$newServoDefPulseWidth = document.getElementById('newServoDefPulseWidth');
    DOM.$newServoRaspiId = document.getElementById('newServoRaspiId');
  }

  return {
    init: init
  };
})();
