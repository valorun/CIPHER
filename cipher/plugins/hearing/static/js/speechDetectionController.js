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
    socket.on('chat', (msg) => {
      const className = msg.source === 'robot' ? 'rcvd' : 'sent';
      DOM.$detectionResult.insertAdjacentHTML('beforeend',
        '<div data-time="' + msg.time + '" class="msg ' + className + '">' + msg.message + '</div>'
      );
      DOM.$detectionResult.parentElement.scrollTop = DOM.$detectionResult.parentElement.offsetHeight;
    });
  }

  function cacheDom() {
    DOM.$startStopRecognition = document.getElementById('start-stop-recognition');
    DOM.$speechDetectionModal = document.getElementById('speech-detection-modal');
    DOM.$detectionResult = document.getElementById('detection-result');
  }

  return {
    init: init
  };
})();
