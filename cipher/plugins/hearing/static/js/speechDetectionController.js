/* globals socket */

/* exported speechDetectionController */
const speechDetectionController = (() => {
  'use strict';

  const DOM = {};

  let startStopButtonState = true;

  /* PUBLIC METHODS */
  function init() {
    cacheDom();
    bindUIEvents();
  }

  /* PRIVATE METHODS */
  function bindUIEvents() {
    DOM.$startStopRecognition.addEventListener('click', () => {
      if (startStopButtonState) {
        socket.emit('start_speech_recognition');
        DOM.$startStopRecognition.value = 'Arrêter la reconnaissance';
      } else {
        socket.emit('stop_speech_recognition');
        DOM.$startStopRecognition.value = 'Lancer la reconnaissance';
      }
      startStopButtonState = !startStopButtonState;
    });

    // server response when a sentence must be play on the client
    socket.on('response', (msg) => {
      const time = new Date();
      DOM.$detectionResult.insertAdjacentHTML('beforeend', '<li>' +
      '<div class="row">' +
      '<div class="col l2 m2 s3 center">' +
      '<span class="border circle large btn hover-none"><i class="fas fa-robot fa-fw"></i></span>' +
      '</div>' +
      '<div class="container round-large light-grey border col l10 m10 s9">' +
      '<div class="left-align"><p>' +
      msg +
      '</p></div>' +
      '<div class="right-align"><p>' + time.getHours() + ':' + time.getMinutes() + '</p></div>' +
      '</div>' +
      '</div>' +
      '</li>');
      DOM.$detectionResult.parentElement.scrollTop = DOM.$detectionResult.parentElement.offsetHeight;
    });
  }

  function cacheDom() {
    DOM.$startStopRecognition = document.getElementById('startStopRecognition');
    DOM.$speechDetectionModal = document.getElementById('speechDetectionModal');
    DOM.$detectionResult = document.getElementById('detectionResult');
  }

  return {
    init: init
  };
})();
