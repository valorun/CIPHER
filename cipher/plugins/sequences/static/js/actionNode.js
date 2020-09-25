'use strict';

/* exported ActionNode */
class ActionNode {
  constructor(name) {
    if (new.target === ActionNode) {
      throw new TypeError('Cannot construct ActionNode instances directly');
    }
    this.action = {};
    this.action.name = name;
    this.action.parameters = {};
    this.shape = 'image';
    this.font = {};
    this.font.face = 'Electrolize';
    this.label = '';
    this.image = '/sequences/static/img/' + name + '.png';
  }

  static fromJSON(json) {
    if (!('name' in json)) {
      throw new TypeError('Invalid JSON ActionNode format');
    }

    switch (json.name) {
      case 'relay':
        return new RelayAction(json.parameters.label, json.parameters.state);
      case 'sound':
        return new SoundAction(json.parameters.name);
      case 'speech':
        return new SpeechAction(json.parameters.text);
      case 'motion':
        return new MotionAction(json.parameters.direction, json.parameters.speed);
      case 'servo':
        return new ServoAction(json.parameters.label, json.parameters.position, json.parameters.speed);
      case 'servoSequence':
        return new ServoSequenceAction(json.parameters.index);
      default:
        return new CustomAction(json.name, json.parameters);
        // throw new TypeError('Invalid JSON ActionNode format');
    }
  }

  toJSON() {
    return {
      id: this.id,
      action: this.action
    };
  }
}

/* exported RelayAction */
class RelayAction extends ActionNode {
  constructor(label, state) {
    super('relay');
    if (!label || label === '') {
      throw new TypeError('No relay parameter selected');
    }
    this.action.parameters.label = label;
    this.action.parameters.state = state;
    this.label = label + '⇨' + state;
  }
}

/* exported SoundAction */
class SoundAction extends ActionNode {
  constructor(name) {
    super('sound');
    if (!name || name === '') {
      throw new TypeError('No sound parameter selected');
    }

    this.action.parameters.name = name;
    this.label = name;
  }
}

/* exported SpeechAction */
class SpeechAction extends ActionNode {
  constructor(text) {
    super('speech');
    this.action.parameters.text = text;

    this.label = '"' + text + '"';
  }
}

/* exported MotionAction */
class MotionAction extends ActionNode {
  constructor(direction, speed) {
    super('motion');
    if (!direction || direction === '') {
      throw new TypeError('No direction parameter selected');
    }
    this.action.parameters.direction = direction;
    this.action.parameters.speed = speed;

    this.label = direction + ' | ' + speed + '%';
  }
}

/* exported ServoAction */
class ServoAction extends ActionNode {
  constructor(label, position, speed) {
    super('servo');
    if (!label || label === '') {
      throw new TypeError('No label parameter selected');
    }
    this.action.parameters.label = label;
    this.action.parameters.position = position;
    this.action.parameters.speed = speed;
    this.label = label + '⇨' + position + ' | ' + speed + '%';
  }
}
ServoAction.MAX_SPEED = 100;
ServoAction.MIN_SPEED = 0;

/* exported ServoSequenceAction */
class ServoSequenceAction extends ActionNode { // COMPATIBILITY REASON
  constructor(index) {
    super('servoSequence');
    if (index === undefined || index === '') {
      throw new TypeError('Invalid sequence parameter');
    }

    this.action.parameters.index = index;
    this.image = '/sequences/static/img/servo.png';
    this.label = index + '';
  }
}

/* exported CustomAction */
class CustomAction extends ActionNode {
  constructor(name, parameters) {
    super(name);
    this.action.parameters = parameters;
    this.label = name + ': ' + JSON.stringify(parameters);
    this.image = '/sequences/static/img/default.png';
  }
}
