/* globals socket */

/* exported servosController */
const servosController = (() => {
  'use strict';

  const DOM = {};

  let servos = [];

  class Servo {
    constructor($tr) {
      this.label = $tr.id;
      this.$range = document.getElementById(this.label + '-range');
      this.$valueDisplay = document.getElementById(this.label + '-value');
      this.$speed = document.getElementById(this.label + '-speed');
      this.$reset = document.getElementById(this.label + '-reset');
      this.defaultValue = parseInt(this.$reset.dataset.default);

      this.$range.addEventListener('change', e => { this.updateValue(e.target.value); });
      this.$reset.addEventListener('click', e => { this.updateValue(this.defaultValue); });
    }

    updateValue(newValue) {
      this.value = newValue;
      this.$valueDisplay.innerHTML = newValue;
      this.$range.value = newValue;
      socket.emit('action', 'servo', { label: this.label, position: parseInt(newValue), speed: parseInt(this.$speed.value) });
    }
  }

  /* PUBLIC METHODS */
  function init() {
    cacheDom();
    bindUIEvents();
  }

  /* PRIVATE METHODS */
  function bindUIEvents() {
    servos = [...document.getElementById('servos-table').rows].slice(1).map(element => new Servo(element));
  }

  function cacheDom() {
  }

  return {
    init: init
  };
})();
