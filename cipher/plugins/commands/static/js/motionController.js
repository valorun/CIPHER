/* globals socket */
/* globals templateController */

/* exported motionController */
const motionController = (() => {
  'use strict';

  const DOM = {};

  let keyPressed = false;

  /* PUBLIC METHODS */
  function init() {
    cacheDom();
    bindUIEvents();
  }

  /* PRIVATE METHODS */
  function bindUIEvents() {
    // selects different listeners depending on the type of device used.
    let startActionEvent = 'mousedown';
    let stopActionEvent = 'mouseup'; // mouseleave if we also want to stop when the cursor is out of the button
    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini|Mobile|Windows Phone|Lumia|Tablet/i.test(navigator.userAgent)) {
      startActionEvent = 'touchstart';
      stopActionEvent = 'touchend';
    }

    // carriage panel controller
    [...document.getElementsByClassName('motion-direction')].forEach(e => {
      const direction = e.getAttribute('value').split('-')[1];
      e.addEventListener(startActionEvent, () => {
        const speed = parseInt(DOM.$motionSpeed.value);
        console.log(direction + ', ' + speed);
        socket.emit('action', 'motion', { direction: direction, speed: speed });
      });
      e.addEventListener(stopActionEvent, () => {
        console.log('stop, 0');
        socket.emit('action', 'motion', { direction: 'stop', speed: 0 });
      });
    });

    // carriage key controller
    document.addEventListener('keydown', (e) => {
      if (!templateController.getAccordion('motion').isOpen) {
        return;
      }
      e.preventDefault();
      if (keyPressed) {
        return;
      }
      let direction = 'stop';
      const speed = parseInt(DOM.$motionSpeed.value);
      switch (e.key) {
        case 'ArrowLeft':
          direction = 'left';
          break;
        case 'ArrowUp':
          direction = 'forwards';
          break;
        case 'ArrowRight':
          direction = 'right';
          break;
        case 'ArrowDown':
          direction = 'backwards';
          break;
      }
      console.log(direction + ', ' + speed);
      socket.emit('action', 'motion', { direction: direction, speed: speed });
      keyPressed = true;
    });

    document.addEventListener('keyup', () => {
      if (!templateController.getAccordion('motion').isOpen) {
        return;
      }
      console.log('stop, 0');
      socket.emit('action', 'motion', { direction: 'stop', speed: 0 });
      keyPressed = false;
    });
  }

  function cacheDom() {
    DOM.$motionSpeed = document.getElementById('motion-speed');
  }

  return {
    init: init
  };
})();
