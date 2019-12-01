/* globals socket */

'use strict';

/* exported CommandButton */
class CommandButton {
	
	/**
	 * 
	 * @param {string} label 
	 * @param {string} color 
	 */
	constructor(label, type, color){
		if (new.target === CommandButton) {
			throw new TypeError('Cannot construct CommandButton instances directly');
		}
		this.label = label;
		this.action = {};
		this.action.type = type;
		this.color = color;
		this.$el = document.createElement('button');
		this.$el.id = '_' + Math.random().toString(36).substr(2, 9);

		this.$el.classList.add('btn');
		if(color != null) {
			this.$el.dataset.color = color;
			this.$el.classList.add(color);
		}
		this.$el.innerHTML = label;
	}

	show() {
		this.$el.classList.remove('hide');
	}

	hide() {
		this.$el.classList.add('hide');
	}

	enable() {
		this.$el.classList.remove('disabled');
	}

	disable() {
		this.$el.classList.add('disabled');
	}

	addEventListener(event, callback) {
		this.$el.addEventListener(event, callback);
	}

	executeAction() {
		console.log('Executed action: ' + JSON.stringify(this.action));
	}

	static fromJSON(json){
		if(!('action' in json) || !('type' in json.action))
			throw new TypeError('Invalid JSON CommandButton format');

		switch (json.action.type) {
		case 'relay':
			return new RelayButton(json.label, json.action.relay, json.color);
		case 'sound':
			return new SoundButton(json.label, json.action.sound, json.color);
		case 'sequence':
			return new SequenceButton(json.label, json.action.sequence, json.color);
		default:
			throw new TypeError('Invalid JSON CommandButton format');
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
		if(!relay)
			throw new TypeError('Invalid relay parameter');

		this.action.relay = relay;
	}

	executeAction() {
		super.executeAction();
		socket.emit('activate_relay', this.action.relay);
	}

	activate() {
		this.$el.classList.add('border-green');
		this.$el.classList.remove('border-dark-red');
	}

	desactivate() {
		this.$el.classList.add('border-dark-red');
		this.$el.classList.remove('border-green');
	}
}

/* exported SoundButton */
class SoundButton extends CommandButton {
	constructor(label, sound, color) {
		super(label, 'sound', color);
		if(!sound)
			throw new TypeError('Invalid sound parameter');

		this.action.sound = sound;
	}

	executeAction() {
		super.executeAction();
		socket.emit('play_sound', this.actionParameter);
	}
}

/* exported SequenceButton */
class SequenceButton extends CommandButton {
	constructor(label, sequence, color) {
		super(label, 'sequence', color);
		if(!sequence)
			throw new TypeError('Invalid sequence parameter');

		this.action.sequence = sequence;
	}

	executeAction() {
		super.executeAction();
		socket.emit('play_sequence', this.actionParameter);
	}
}