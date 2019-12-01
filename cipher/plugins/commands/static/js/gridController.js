/* globals CommandButton */
/* globals RelayButton */
/* globals DraggablesGrid */

/* exported gridController */
const gridController = (() => {
	'use strict';
	
	const DOM = {};

	const buttons = [];
	let grid = null;


	/* PUBLIC METHODS */
	function init() {
		cacheDom();
		bindUIEvents();
		grid.addCells(30);
	}

	function addButton(buttonData, index = 0) {
		if (actionAlreadyUsed(buttonData.action))
			throw new AlreadyUsedError('Action is already used');
		const newButton = CommandButton.fromJSON(buttonData);
		grid.addDraggableElement(newButton.$el, index);
		buttons.push(newButton);
		return newButton;
	}

	function disableButtons() {
		buttons.forEach(b => {
			b.disable();
		});
		grid.enableDrag();
	}

	function enableButtons() {
		buttons.forEach(b => {
			b.enable();
		});
		grid.disableDrag();
	}

	function updateRelayButtons(relaysStates) {
		//get the relays and update the associated state
		const relaysButtons = buttons.filter(b => b instanceof RelayButton);
		relaysStates.map(r => r.relay = relaysButtons.find(b => b.action.relay === r.relay))
			.forEach(r => r.state === 1 ? r.relay.activate() : r.relay.desactivate());
	}

	function hideTrashbin() {
		DOM.$trashbin.classList.add('hide');
	}

	function showTrashbin() {
		DOM.$trashbin.classList.remove('hide');
	}

	function clear() {
		grid.clearDraggables();
	}

	function toJSON() {
		return buttons
			.map(b => {
				const json = b.toJSON();
				// add position information
				json.index = grid.draggables.find(d => d.element.innerHTML === b.$el.innerHTML).index;
				return json;
			});
	}

	/* PRIVATE METHODS */
	function bindUIEvents() {
		grid = new DraggablesGrid(DOM.$grid, DOM.$trashbin);
		grid.$grid_element.addEventListener('delete', (e) =>{
			// delete the button assiated with the deleted element
			const buttonIndex = buttons.findIndex(b => b.$el.innerHTML === e.target.innerHTML);
			buttons.splice(buttonIndex, 1);
		});
	}

	function cacheDom() {
		DOM.$trashbin = document.getElementById('trashbin');
		DOM.$grid = document.getElementById('grid');
	}

	/**
	 * Check if a button with the same action already exists
	 */
	function actionAlreadyUsed(action){
		let found = false;
		buttons.forEach(b => {
			if(JSON.stringify(b.action) === JSON.stringify(action)){
				found = true;
				return false;
			}
		});
		return found;
	}

	return {
		init: init,
		addButton: addButton,
		disableButtons: disableButtons,
		enableButtons: enableButtons,
		updateRelayButtons: updateRelayButtons,
		hideTrashbin: hideTrashbin,
		showTrashbin: showTrashbin,
		clear: clear,
		toJSON: toJSON
	};
})();

/* exported AlreadyUsedError */
class AlreadyUsedError extends Error {
	constructor(...params) {
		super(...params);
	
		if(Error.captureStackTrace) {
			Error.captureStackTrace(this, AlreadyUsedError);
		}
		this.name = 'AlreadyUsedError';
	}
}