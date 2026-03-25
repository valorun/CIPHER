/* globals socket, fetchJson */

/* exported speechDetectionController */
const speechDetectionController = (() => {
  'use strict';

  const DOM = {};

  let startStopButtonState = true;

  /* PUBLIC METHODS */
  function init() {
    cacheDom();
    bindUIEvents();
    // Scroll to bottom of chat by default
    DOM.$detectionResult.scrollTop = DOM.$detectionResult.scrollHeight;
  }

  /* PRIVATE METHODS */
  function bindUIEvents() {
    DOM.$startStopRecognition.addEventListener('click', () => {
      if (startStopButtonState) {
        socket.emit('start_speech_recognition');
        DOM.$startStopRecognition.innerHTML = '<i class="fas fa-microphone-slash"></i> Arrêter la reconnaissance';
      } else {
        socket.emit('stop_speech_recognition');
        DOM.$startStopRecognition.innerHTML = '<i class="fas fa-microphone"></i> Lancer la reconnaissance';
      }
      startStopButtonState = !startStopButtonState;
    });

    DOM.$sendManualTranscript.addEventListener('click', () => {
        const transcript = DOM.$manualTranscript.value;
        if (transcript) {
            fetchJson('/text_input', 'POST', { transcript: transcript })
              .then(() => {
                console.log('Text input processed');
                DOM.$manualTranscript.value = '';
              });
        }
    });

    DOM.$resetChat.addEventListener('click', () => {
        fetch('/reset_chat', { method: 'POST' })
            .then(r => console.log('Chat reset requested'));
    });

    // server response when a sentence must be play on the client
    socket.on('chat', (msg) => {
      const className = msg.source === 'robot' ? 'rcvd' : 'sent';
      DOM.$detectionResult.insertAdjacentHTML('beforeend',
        '<div data-time="' + msg.time + '" class="msg ' + className + '">' + msg.message + '</div>'
      );
      DOM.$detectionResult.scrollTop = DOM.$detectionResult.scrollHeight;
    });

    socket.on('clear_chat', () => {
        DOM.$detectionResult.innerHTML = '';
    });

    // Delete memory
    document.querySelectorAll('.delete-memory-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        if(confirm("Êtes-vous sûr de vouloir supprimer ce souvenir ?")) {
          const memoryId = e.currentTarget.getAttribute('data-id');
          fetchJson('/delete_memory', 'POST', { id: memoryId })
            .then(r => {
              if (typeof successAlert === 'function') {
                  successAlert(r);
              } else {
                  console.log(r);
              }
              const row = document.getElementById('memory-row-' + memoryId);
              if(row) row.remove();
            });
        }
      });
    });

  }

  function cacheDom() {
    DOM.$startStopRecognition = document.getElementById('start-stop-recognition');
    DOM.$speechDetectionModal = document.getElementById('speech-detection-modal');
    DOM.$detectionResult = document.getElementById('detection-result');
    DOM.$manualTranscript = document.getElementById('manual-transcript');
    DOM.$sendManualTranscript = document.getElementById('send-manual-transcript');
    DOM.$resetChat = document.getElementById('reset-chat');
  }

  return {
    init: init
  };
})();
