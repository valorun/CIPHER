/* exported speechNotConnectedController */
const speechNotConnectedController = (() => {
  'use strict';

  /* PUBLIC METHODS */
  function init() {
    setTimeout(() => {
      window.location.reload(1);
    }, 5000);
  }

  return {
    init: init
  };
})();
