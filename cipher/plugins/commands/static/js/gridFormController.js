/* globals failAlert */
/* globals socket */
/* globals fetchJson */
/* globals colorpickerController */
/* globals gridController */
/* globals AlreadyUsedError */


/* exported gridFormController */
const gridFormController = (() => {
	'use strict';
	const colorpicker = colorpickerController;
	const grid = gridController;

	let editionMode = false;
	const DOM = {};


	/* PUBLIC METHODS */
	function init() {
		colorpicker.init();
		grid.init();
		cacheDom();
		bindUIEvents();
		// initialize the grid at his initial state in disabled edition mode
		loadGrid();
		disableEditionMode();
	}

	/* PRIVATE METHODS */
	function bindUIEvents() {

		document.getElementById('addButton').addEventListener('click', addButton);

		DOM.$buttonType.addEventListener('change', () => {
			updateForm();
		});

		DOM.$editPanelButton.addEventListener('click', () => {
			updateMode();
			saveGrid();
		});

		// update status information about a specified relay
		socket.on('receive_relays_state', (relaysStates) => 
			grid.updateRelaysButtons(relaysStates));
	}

	function cacheDom() {
		DOM.$buttonLabel = document.getElementById('buttonLabel');
		DOM.$buttonType = document.querySelector('select[name=newButtonTypeChoice]');
		DOM.$relays = document.getElementById('relays');
		DOM.$sequences = document.getElementById('sequences');
		DOM.$sounds = document.getElementById('sounds');

		DOM.$editPanelButton = document.getElementById('editPanelButton');
		DOM.$newButtonPanel = document.getElementById('newButtonPanel');

		DOM.$relayOptions = document.getElementById('relayOptions');
		DOM.$sequenceOptions = document.getElementById('sequenceOptions');
		DOM.$soundOptions = document.getElementById('soundOptions');
	}


	/**
	 * Add a button to the grid
	 * An action is associated. Additional parameters can be specified
	 */
	function addButton(){
		const buttonData = {};
		buttonData.action= {};
		buttonData.action.type = DOM.$buttonType.value;
		buttonData.label = DOM.$buttonLabel.value;
		buttonData.color = colorpicker.getSelectedColor();

		if (DOM.$buttonType.value === 'relay') {
			if(DOM.$relays.value === ''){
				failAlert('Aucun relai n\'a été selectionné.');
				return;
			}
			buttonData.action.relay = DOM.$relays.value;
		} else if (DOM.$buttonType.value === 'sequence') {
			if(DOM.$sequences.value === ''){
				failAlert('Aucune séquence n\'a été selectionnée.');
				return;
			}
			buttonData.action.sequence = DOM.$sequences.value;
		} else if (DOM.$buttonType.value === 'sound') {
			if(DOM.$sounds.value === ''){
				failAlert('Aucun son n\'a été selectionné.');
				return;
			}
			buttonData.action.sound = DOM.$sounds.value;
		}

		
		try {
			const newButton = grid.addButton(buttonData);
			
			if(editionMode)
				newButton.disable();
			
		} catch (e) {
			console.error(e);
			if(e instanceof AlreadyUsedError)
				failAlert('Un bouton correspondant à la même action existe déjà');
			
			return false;
		}
		
		return true;
	}

	/**
	 * Load the grid from the server
	 */
	function loadGrid(){
		grid.clear();
		fetchJson('/load_buttons', 'POST')
			.then(data => {
				data.forEach((button) => {
					grid.addButton(button, button.index);
				});
				socket.emit('get_relays_state');
			});

		return false;
	}

	/**
	 * Save the grid on the server
	 */
	function saveGrid() {
		console.log(grid.toJSON());
		fetchJson('/save_buttons', 'POST', {data: JSON.stringify(grid.toJSON())})
			.then(() => {
				console.log('Buttons saved');
			});
	}

	/**
	 * Enable edition mode, the buttons can not be clicked, but can be moved
	 */
	function enableEditionMode(){
		editionMode = true;
		grid.disableButtons();
		DOM.$editPanelButton.classList.add('fa-check');
		DOM.$editPanelButton.classList.remove('fa-edit');
		DOM.$newButtonPanel.classList.remove('hide');
		
	}

	/**
	 * Disable edition mode, the buttons can not be moved, but can be clicked
	 */
	function disableEditionMode(){
		editionMode = false;
		grid.enableButtons();
		DOM.$editPanelButton.classList.remove('fa-check');
		DOM.$editPanelButton.classList.add('fa-edit');
		DOM.$newButtonPanel.classList.add('hide');
	}

	/**
	 * Update the display to match the selected mode
	 */
	function updateMode(){
		if(editionMode){
			disableEditionMode();
		}
		else{
			enableEditionMode();
		}
	}

	/**
	 * Update the form to match selected options
	 */
	function updateForm() {
		DOM.$relayOptions.classList.add('hide');
		DOM.$sequenceOptions.classList.add('hide');
		DOM.$soundOptions.classList.add('hide');

		if(DOM.$buttonType.value !== '') {
			document.getElementById(DOM.$buttonType.value + 'Options').classList.remove('hide');
		}
		else{
			failAlert('Aucun type de bouton n\'a été selectionné !');
		}
	}

	return {
		init: init,
	};
})();