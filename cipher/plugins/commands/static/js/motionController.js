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
      const direction = e.getAttribute('value').split('_')[1];
      e.addEventListener(startActionEvent, () => {
        const speed = DOM.$motion_speed.value;
        console.log(direction + ', ' + speed);
        socket.emit('motion', direction, speed);
      });
      e.addEventListener(stopActionEvent, () => {
        console.log('stop, 0');
        socket.emit('motion', 'stop', 0);
      });
    });

    // carriage key controller
    document.addEventListener('keydown', (e) => {
      if (!templateController.getAccordion('motion').isOpen) {
        return;
      }
      if (keyPressed) {
        return;
      }
      e.preventDefault();
      let direction = 'stop';
      const speed = DOM.$motion_speed.value;

      switch (e.keyCode) {
        case 37:
          direction = 'left';
          break;
        case 38:
          direction = 'forwards';
          break;
        case 39:
          direction = 'right';
          break;
        case 40:
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
      socket.emit('action', 'motion', { direction: 'stop' });
      keyPressed = false;
    });
  }

  function cacheDom() {
    DOM.$motion_speed = document.getElementById('motion_speed');
  }

  return {
    init: init
  };
})();
