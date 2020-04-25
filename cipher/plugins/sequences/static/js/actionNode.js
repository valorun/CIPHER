'use strict';

/* exported ActionNode */
class ActionNode {
  constructor(type) {
    if (new.target === ActionNode) {
      throw new TypeError('Cannot construct ActionNode instances directly');
    }
    this.action = {};
    this.action.type = type;
    this.shape = 'image';
    this.font = {};
    this.font.face = 'Electrolize';
    this.label = '';
    this.image = '/sequences/static/img/' + type + '.png';
  }

  static fromJSON(json) {
    if (!('type' in json)) {
      throw new TypeError('Invalid JSON ActionNode format');
    }

    switch (json.type) {
      case 'relay':
        return new RelayAction(json.relay, json.state);
      case 'sound':
        return new SoundAction(json.sound);
      case 'speech':
        return new SpeechAction(json.speech);
      case 'script':
        return new ScriptAction(json.script);
      case 'motion':
        return new MotionAction(json.direction, json.speed);
      case 'servo':
        return new ServoAction(json.servo, json.position, json.position, json.position, json.speed);
      case 'servoSequence':
        return new ServoSequenceAction(json.sequence);
      case 'pause':
        return new PauseAction(json.time);
      default:
        throw new TypeError('Invalid JSON ActionNode format');
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
  constructor(relay, state) {
    super('relay');
    if (!relay || relay === '') {
      throw new TypeError('Invalid relay parameter');
    }

    this.action.relay = relay;
    this.action.state = state;
    this.label = relay + '⇨' + state;
  }
}

/* exported SoundAction */
class SoundAction extends ActionNode {
  constructor(sound) {
    super('sound');
    if (!sound || sound === '') {
      throw new TypeError('Invalid sound parameter');
    }

    this.action.sound = sound;
    this.label = sound;
  }
}

/* exported SpeechAction */
class SpeechAction extends ActionNode {
  constructor(speech) {
    super('speech');
    this.action.speech = speech;

    this.label = '"' + speech + '"';
  }
}

/* exported ScriptAction */
class ScriptAction extends ActionNode {
  constructor(script) {
    super('script');
    if (!script || script === '') {
      throw new TypeError('Invalid script parameter');
    }

    this.action.script = script;
    this.label = script;
  }
}

/* exported MotionAction */
class MotionAction extends ActionNode {
  constructor(direction, speed) {
    super('motion');
    if (!direction || direction === '') {
      throw new TypeError('Invalid direction parameter');
    }
    if (!isNumberBetween(speed, MotionAction.MIN_SPEED, MotionAction.MAX_SPEED)) {
      throw new RangeError('Speed must be a value between ' + MotionAction.MIN_SPEED + ' and ' + MotionAction.MAX_SPEED);
    }
    this.action.direction = direction;
    this.action.speed = speed;

    this.label = direction + ' | ' + speed + '%';
  }
}
MotionAction.MAX_SPEED = 100;
MotionAction.MIN_SPEED = 0;

/* exported ServoAction */
class ServoAction extends ActionNode {
  constructor(servo, position, minPulseWidth, maxPulseWidth, speed) {
    super('servo');
    if (!servo || servo === '') {
      throw new TypeError('Invalid servo parameter');
    }
    if (!isNumberBetween(speed, ServoAction.MIN_SPEED, ServoAction.MAX_SPEED)) {
      throw new RangeError('Speed must be a value between ' + ServoAction.MIN_SPEED + ' and ' + ServoAction.MAX_SPEED);
    }
    if (!isNumberBetween(position, minPulseWidth, maxPulseWidth)) {
      throw new RangeError('Position must be a value between ' + minPulseWidth + ' and ' + maxPulseWidth);
    }
    this.action.servo = servo;
    this.action.position = position;
    this.action.speed = speed;
    this.label = servo + '⇨' + position + ' | ' + speed + '%';
  }
}
ServoAction.MAX_SPEED = 100;
ServoAction.MIN_SPEED = 0;

/* exported ServoSequenceAction */
class ServoSequenceAction extends ActionNode { // COMPATIBILITY REASON
  constructor(sequence) {
    super('servoSequence');
    if (sequence === undefined || sequence === '') {
      throw new TypeError('Invalid sequence parameter');
    }

    this.action.sequence = sequence;
    this.image = '/sequences/static/img/servo.png';
    this.label = sequence + '';
  }
}

/* exported PauseAction */
class PauseAction extends ActionNode {
  constructor(time) {
    super('pause');
    if (isNaN(time) || time < 0) {
      throw new TypeError('Invalid sequence parameter');
    }

    this.action.time = time;
    this.label = time + 'ms';
  }
}

function isNumberBetween(value, min, max) {
  return !isNaN(parseInt(value)) && value <= max && value >= min;
}
