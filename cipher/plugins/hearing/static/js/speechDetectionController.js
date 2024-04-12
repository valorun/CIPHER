/* globals socket */

/* exported speechDetectionController */
const speechDetectionController = (() => {
  'use strict';

  const DOM = {};

  let toggleButtonState = true;

  /* PUBLIC METHODS */
  function init() {
    cacheDom();
    bindUIEvents();
  }

  /* PRIVATE METHODS */
  function bindUIEvents() {
    DOM.$toggleRecognition.addEventListener('click', () => {
      if (toggleButtonState) {
        socket.emit('enable_speech_recognition');
        DOM.$toggleRecognition.value = 'Désactiver la reconnaissance';
      } else {
        socket.emit('disable_speech_recognition');
        DOM.$toggleRecognition.value = 'Activer la reconnaissance';
      }
      toggleButtonState = !toggleButtonState;
    });

    DOM.$triggerRecognition.addEventListener('click', () => {
        socket.emit('trigger_speech_recognition');
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
    DOM.$toggleRecognition = document.getElementById('toggle-recognition');
    DOM.$triggerRecognition = document.getElementById('trigger-recognition');
    DOM.$speechDetectionModal = document.getElementById('speech-detection-modal');
    DOM.$detectionResult = document.getElementById('detection-result');
  }

  return {
    init: init
  };
})();
