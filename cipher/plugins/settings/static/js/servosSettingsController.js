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
      this.label = $tr.id;
      this.$label = document.getElementById(this.$tr.id + '_label');
      this.$pin = document.getElementById(this.$tr.id + '_pin');
      this.$min = document.getElementById(this.$tr.id + '_min');
      this.$max = document.getElementById(this.$tr.id + '_max');
      this.$default = document.getElementById(this.$tr.id + '_default');
      this.$raspi = document.getElementById(this.$tr.id + '_raspi');

      this.$delete = document.getElementById(this.$tr.id + '_delete');
      this.$save = document.getElementById(this.$tr.id + '_save');
      this.$enable = document.getElementById(this.$tr.id + '_enable');

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
        servo_label: this.label,
        new_servo_label: this.$label.value,
        servo_pin: this.$pin.value,
        raspi_id: this.$raspi.value,
        min_pulse_width: this.$min.value,
        max_pulse_width: this.$max.value,
        def_pulse_width: this.$default.value
      }).then((r) => {
        successAlert(r);
        console.log(this.label + ' updated');
        this.label = this.$label.value;
        this.$tr.id = this.label;
        this.$label.id = this.label + '_label';
        this.$pin.id = this.label + '_pin';
        this.$min.id = this.label + '_min';
        this.$max.id = this.label + '_max';
        this.$default.id = this.label + '_default';
      });
    }

    /**
     * Delete the servo
     */
    delete() {
      const confirm = window.confirm('Etes vous sûr de vouloir supprimer le servomoteur \'' + this.label + '\' ?');
      if (confirm) {
        fetchJson('/delete_servo', 'POST', { servo_label: this.label })
          .then((r) => {
            successAlert(r);
            console.log(this.label + ' deleted');
            const el = document.getElementById(this.label);
            el.parentNode.removeChild(el);
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
      fetchJson('/enable_servo', 'POST', { servo_label: this.label, value: value })
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
          servo_label: DOM.$newServoLabel.value,
          servo_pin: DOM.$newServoPin.value,
          min_pulse_width: DOM.$newServoMinPulseWidth.value,
          max_pulse_width: DOM.$newServoMaxPulseWidth.value,
          def_pulse_width: DOM.$newServoDefPulseWidth.value,
          raspi_id: DOM.$newServoRaspiId.value
        }).then(() => {
        location.reload();
      });
    });

    // remove servo entry from list when its element is deleted
    servosEntries = Array.from(document.getElementById('servos_table').rows).slice(1).map(element => new ServoEntry(element));
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
