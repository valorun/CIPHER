/* globals CommandButton */
/* globals RelayButton */
/* globals GridItem */
/* globals Muuri */

/* exported gridController */
const gridController = (() => {
	'use strict';
	
	const DOM = {};

	let grid = null;
	const gridItems = [];


	/* PUBLIC METHODS */
	function init() {
		cacheDom();
		bindUIEvents();
	}

	function addButton(buttonData, index = 0) {
		if (actionAlreadyUsed(buttonData.action))
			throw new AlreadyUsedError('Action is already used');
		const newButton = CommandButton.fromJSON(buttonData);

		// containers elements needed for animation and position
		const $outerWrapper = document.createElement('div');
		$outerWrapper.classList.add('grid-item');
		const $innerWrapper = document.createElement('div');
		$innerWrapper.classList.add('grid-item-content');
		$innerWrapper.appendChild(newButton.$el);
		$outerWrapper.appendChild($innerWrapper);

		const newItem = grid.add($outerWrapper, {index: index});
		newItem.commandButton = newButton; // link grid item to our custom button object

		const newGridItem = new GridItem(newButton, newItem[0]);
		newGridItem.onClose((gridItem) => {
			const buttonIndex = gridItems.findIndex(gi => JSON.stringify(gi.commandButton) === JSON.stringify(gridItem.commandButton) );
			gridItems.splice(buttonIndex, 1);
			grid.remove(gridItem.item, {removeElements: true});
		});

		gridItems.push(newGridItem);
		
		return newButton;
	}

	function disableButtons() {
		gridItems.forEach(gi => {
			gi.commandButton.disable();
		});
	}

	function enableButtons() {
		gridItems.forEach(gi => {
			gi.commandButton.enable();
		});
	}

	function updateRelayButtons(relaysStates) {
		// get the relays and update the associated state
		const relaysButtons = gridItems.map(gi => gi.commandButton).filter(b => b instanceof RelayButton);
		relaysStates.map(r => r.relay = relaysButtons.find(b => b.action.relay === r.relay))
			.forEach(r => r.state === 1 ? r.relay.activate() : r.relay.desactivate());
	}

	function clear() {
		grid.remove(grid.getItems(), {removeElements: true});
	}

	function toJSON() {
		return gridItems
			.map(gi => {
				const json = gi.commandButton.toJSON();
				// add position information
				json.index = grid.getItems().findIndex(item => item.getElement().innerHTML === gi.item.getElement().innerHTML);
				return json;
			});
	}

	/* PRIVATE METHODS */
	function bindUIEvents() {
		grid = new Muuri('.grid', {dragEnabled: true});
	}

	function cacheDom() {
		DOM.$grid = document.getElementById('grid');
	}

	/**
	 * Check if a button with the same action already exists
	 */
	function actionAlreadyUsed(action){
		let found = false;
		gridItems.map(gi => gi.commandButton).forEach(b => {
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