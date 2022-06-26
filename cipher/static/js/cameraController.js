/* globals socket */

/* exported cameraController */
const cameraController = (() => {
  'use strict';

  const DOM = {};

  let isPlaying = true;

  /* PUBLIC METHODS */
  function init() {
    cacheDom();
    bindSocketIOEvents();
    bindUIEvents();
  }

  /* PRIVATE METHODS */
  function bindUIEvents() {
    DOM.$start_camera_button.addEventListener('click', () => {
      if (DOM.$start_camera_button.classList.contains('fa-play')) {
        socket.emit('start_camera_stream');
      } else {
        socket.emit('stop_camera_stream');
      }
    });
  }

  function bindSocketIOEvents() {
    socket.on('camera_stream_data', (msg) => {
      DOM.$camera.src = msg;
      if (isPlaying) {
        DOM.$start_camera_button.classList.add('fa-pause');
        DOM.$start_camera_button.classList.remove('fa-play');
        isPlaying = false;
      }
    });

    socket.on('started_camera_stream', () => {
      isPlaying = true;
    });

    socket.on('stopped_camera_stream', () => {
      DOM.$start_camera_button.classList.add('fa-play');
      DOM.$start_camera_button.classList.remove('fa-pause');
    });
  }

  function cacheDom() {
    DOM.$start_camera_button = document.getElementById('start-camera-button');
    DOM.$camera = document.getElementById('camera');
  }

  return {
    init: init
  };
})();
