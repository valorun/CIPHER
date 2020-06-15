/* globals socket */

/* exported debugController */
const debugController = (() => {
  'use strict';

  const DOM = {};

  let servos = [];

  class Servo {
    constructor($tr) {
      this.label = $tr.id;
      this.$range = document.getElementById(this.label + '_range');
      this.$valueDisplay = document.getElementById(this.label + '_value');
      this.$speed = document.getElementById(this.label + '_speed');
      this.$reset = document.getElementById(this.label + '_reset');
      this.defaultValue = parseInt(this.$reset.dataset.default);

      this.$range.addEventListener('change', e => { this.updateValue(e.target.value); });
      this.$reset.addEventListener('click', e => { this.updateValue(this.defaultValue); });
    }

    updateValue(newValue) {
      this.value = newValue;
      this.$valueDisplay.innerHTML = newValue;
      this.$range.value = newValue;
      socket.emit('action', 'servo', { label: this.label, position: newValue, speed: parseInt(this.$speed.value) });
    }
  }

  /* PUBLIC METHODS */
  function init() {
    cacheDom();
    bindUIEvents();
  }

  /* PRIVATE METHODS */
  function bindUIEvents() {
    servos = Array.from(document.getElementById('servos_table').rows).slice(1).map(element => new Servo(element));
  }

  function cacheDom() {
  }

  return {
    init: init
  };
})();
