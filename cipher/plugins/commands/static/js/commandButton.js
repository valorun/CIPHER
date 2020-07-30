/* globals socket */

'use strict';

/* exported CommandButton */
class CommandButton {
  /**
  *
  * @param {string} label
  * @param {string} color
  */
  constructor(label, type, color) {
    if (new.target === CommandButton) {
      throw new TypeError('Cannot construct CommandButton instances directly');
    }
    this.label = label;
    this.action = {};
    this.action.type = type;
    this.color = color;

    this.$el = document.createElement('div');

    this.$button = document.createElement('button');
    this.$button.id = '_' + Math.random().toString(36).substr(2, 9);
    this.$button.classList.add('button', 'display-container');
    if (color != null) {
      this.$button.dataset.color = color;
      this.$button.classList.add(color);
    }
    this.$button.innerHTML = label;
    this.$el.appendChild(this.$button);

    // cross element
    this.$cross = document.createElement('span');
    this.$cross.type = 'button';
    this.$cross.classList.add('button', 'display-topright');
    this.$cross.innerHTML = '&times';
    this.$el.appendChild(this.$cross);

    this.addEventListener('click', () => {
      if (!this.$button.classList.contains('disabled')) {
        this.executeAction();
      }
    });
    this.enable();
  }

  show() {
    this.$el.classList.remove('hide');
  }

  hide() {
    this.$el.classList.add('hide');
  }

  enable() {
    this.$button.classList.remove('disabled');
    this.$cross.classList.add('hide');
  }

  disable() {
    this.$button.classList.add('disabled');
    this.$cross.classList.remove('hide');
  }

  addEventListener(event, callback) {
    this.$button.addEventListener(event, callback);
  }

  executeAction() {
    console.log('Executed action: ' + JSON.stringify(this.action));
  }

  static fromJSON(json) {
    if (!('action' in json) || !('name' in json.action)) {
      throw new TypeError('Invalid JSON CommandButton format');
    }
    switch (json.action.name) {
      case 'relay':
        return new RelayButton(json.label, json.action.label, json.color);
      case 'sequence':
        return new SequenceButton(json.label, json.action.parameters.name, json.color);
      default:
        return new GenericActionButton(json.label, json.action, json.color);
    }
  }

  toJSON() {
    return {
      label: this.label,
      action: this.action,
      color: this.color
    };
  }
}

/* exported RelayButton */
class RelayButton extends CommandButton {
  constructor(label, relay, color) {
    super(label, 'relay', color);
    if (!relay) {
      throw new TypeError('Invalid relay parameter');
    }
    this.action.relay = relay;

    this.$button.style.border = '4px solid';
    this.deactivate();
  }

  executeAction() {
    super.executeAction();
    socket.emit('action', 'relay', { label: this.action.relay });
  }

  activate() {
    this.$button.classList.add('border-green');
    this.$button.classList.remove('border-dark-red');
  }

  deactivate() {
    this.$button.classList.add('border-dark-red');
    this.$button.classList.remove('border-green');
  }
}

/* exported GenericActionButton */
class GenericActionButton extends CommandButton {
  constructor(label, action, color) {
    super(label, 'sound', color);
    if (!action) {
      throw new TypeError('Invalid action parameter');
    }
    this.action = action;
  }

  executeAction() {
    super.executeAction();
    socket.emit('action', this.action.name, this.action.parameters);
  }
}

/* exported SequenceButton */
class SequenceButton extends CommandButton {
  constructor(label, sequence, color) {
    super(label, 'sequence', color);
    if (!sequence) {
      throw new TypeError('Invalid sequence parameter');
    }
    this.action.sequence = sequence;
  }

  executeAction() {
    super.executeAction();
    socket.emit('play_sequence', this.action.sequence);
  }
}
