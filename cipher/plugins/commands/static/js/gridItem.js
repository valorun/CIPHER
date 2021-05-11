'use strict';

/* exported GridItem */
class GridItem {
  /**
  *
  * @param {CommandButton} commandButton
  * @param {Item} item
  */
  constructor(commandButton, item) {
    this.commandButton = commandButton;
    this.item = item;
  }

  onClose(callback) {
    this.commandButton.$cross.addEventListener('click', () => {
      callback(this);
    });
  }
}
