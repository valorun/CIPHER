/* globals socket */

/* exported sequenceController */
const sequenceController = (() => {
  'use strict';

  const DOM = {};

  /* PUBLIC METHODS */
  function init() {
    cacheDom();
    bindUIEvents();
  }

  /* PRIVATE METHODS */
  function bindUIEvents() {
    // directly play a sequence in the list
    document.getElementById('playSeqButton').addEventListener('click', () => {
      if (DOM.$sequence.value !== null && DOM.$sequence.value !== '') {
        socket.emit('play_sequence', DOM.$sequence.value);
      }
    });
  }

  function cacheDom() {
    DOM.$sequence = document.getElementById('sequence');
  }

  return {
    init: init
  };
})();
