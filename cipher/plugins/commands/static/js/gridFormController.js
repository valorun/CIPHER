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
  }

  /**
  * Add a button to the grid
  * An action is associated. Additional parameters can be specified
  */
  function addButton() {
    const buttonData = {};
    buttonData.action = {};
    buttonData.action.name = DOM.$buttonType.value;
    buttonData.action.parameters = {};
    buttonData.label = DOM.$buttonLabel.value;
    buttonData.color = colorpicker.getSelectedColor();

    const $parameters = document.querySelectorAll('[id^=' + DOM.$buttonType.value + '_]:not([id$=_options])');
    $parameters.forEach(e => {
      const key = e.id.split(buttonData.action.name + '_')[1];
      if (e.type === 'number') {
        buttonData.action.parameters[key] = parseInt(e.value);
      } else if (e.type === 'checkbox') {
        buttonData.action.parameters[key] = (e.checked ? 1 : 0);
      } else {
        buttonData.action.parameters[key] = e.value;
      }
    });
    let checkPromise;
    if (buttonData.action.name === 'sequence') {
      checkPromise = fetchJson('/check_sequence', 'POST', buttonData.action.parameters);
    } else {
      checkPromise = fetchJson('/check_action_parameters', 'POST', { action_name: buttonData.action.name, parameters: buttonData.action.parameters });
    }
    checkPromise.then(validation => {
      if (!validation[0]) {
        throw new TypeError(validation[1]);
      }

      const newButton = grid.addButton(buttonData);

      if (editionMode) {
        newButton.disable();
      }
    }).catch(error => {
      if (error instanceof AlreadyUsedError) {
        failAlert('Un bouton correspondant à la même action existe déjà');
        return;
      }
      console.error(error);
      failAlert(error.message);
    });
  }

  /**
  * Load the grid from the server
  */
  function loadGrid() {
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
    fetchJson('/save_buttons', 'POST', { data: JSON.stringify(grid.toJSON()) })
      .then(() => {
        console.log('Buttons saved');
      });
  }

  /**
  * Enable edition mode, the buttons can not be clicked, but can be moved
  */
  function enableEditionMode() {
    editionMode = true;
    grid.disableButtons();
    DOM.$editPanelButton.classList.add('fa-check');
    DOM.$editPanelButton.classList.remove('fa-edit');
    DOM.$newButtonPanel.classList.remove('hide');
  }

  /**
  * Disable edition mode, the buttons can not be moved, but can be clicked
  */
  function disableEditionMode() {
    editionMode = false;
    grid.enableButtons();
    DOM.$editPanelButton.classList.remove('fa-check');
    DOM.$editPanelButton.classList.add('fa-edit');
    DOM.$newButtonPanel.classList.add('hide');
  }

  /**
  * Update the display to match the selected mode
  */
  function updateMode() {
    if (editionMode) {
      disableEditionMode();
    } else {
      enableEditionMode();
    }
  }

  /**
  * Update the form to match selected options
  */
  function updateForm() {
    document.querySelectorAll('[id$=_options]')
      .forEach(e => e.classList.add('hide'));

    if (DOM.$buttonType.value !== '') {
      document.getElementById(DOM.$buttonType.value + '_options').classList.remove('hide');
    } else {
      failAlert('Aucun type de bouton n\'a été selectionné !');
    }
  }

  return {
    init: init
  };
})();
