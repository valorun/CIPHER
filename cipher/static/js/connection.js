/* globals io */

/* exported socket */
const socket = io.connect(window.location.host + '/client');

/* exported connectionManager */
const connectionManager = (() => {
  'use strict';

  let audio = null;

  /* PUBLIC METHODS */
  function init() {
    bindSocketIOEvents();
  }

  /* PRIVATE METHODS */
  function bindSocketIOEvents() {
    socket.on('command', (msg) => {
      console.log('Message from server: ', msg);
    });

    // server response when a sentence must be play on the client
    socket.on('response', (msg) => {
      console.log('Message from server: ', msg);
    });
    socket.on('play_sound', (soundName) => {
      if (audio != null && !audio.ended) {
        audio.pause();
        audio = null;
      } else {
        audio = new Audio(window.location.origin + '/play_sound/' + soundName);
        audio.play();
      }
    });
    socket.on('connect', () => {
      document.getElementById('socketErrorModal').style.display = 'none';
    });
    socket.on('disconnect', () => {
      document.getElementById('socketErrorModal').style.display = 'block';
    });
  }

  return {
    init: init
  };
})();
