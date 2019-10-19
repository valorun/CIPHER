/* globals failAlert */
/* globals templateController */
/* globals graphPanelController */


/* exported graphFormController */
var graphFormController = (() => {
	'use strict';

	let DOM = {};

	let graphPanel = graphPanelController;

	/* PUBLIC METHODS */
	function init() {
		graphPanel.init();
		cacheDom();
		bindUIEvents();
		updateForm();
	}

	/* PRIVATE METHODS */
	function bindUIEvents() {

		document.getElementById('saveButton').addEventListener('click', () => {
			if (graphPanel.graphIsValid())
				saveGraph();
			else {
				failAlert('La séquence n\'est pas valide, certains noeuds n\'ont pas de parent.');
			}
		});

		document.querySelector('select[name=newNodeTypeChoice]').addEventListener('change', () => {
			updateForm();
		});

		document.querySelectorAll('a[name=editSeq]').forEach((e) => {
			e.addEventListener('click', () => {
				let seq_name = e.id.substr(e.id.indexOf('_') + 1);
				console.log(seq_name);

				editSequence(seq_name);
				templateController.getAccordion('creation').open();
				window.location.hash = '#creation';
			});
		});
	}

	function cacheDom() {
		DOM.$motionOptions = document.getElementById('motionOptions');
		DOM.$servoOptions = document.getElementById('servoOptions');
		DOM.$relayOptions = document.getElementById('relayOptions');
		DOM.$speechOptions = document.getElementById('speechOptions');
		DOM.$scriptOptions = document.getElementById('scriptOptions');
		DOM.$soundOptions = document.getElementById('soundOptions');
		DOM.$pauseOptions = document.getElementById('pauseOptions');
		DOM.$servoSequenceOptions = document.getElementById('servoSequenceOptions');
		DOM.$name = document.getElementById('name');
	}

	/**
	 * Update the form to display the options corresponding to the type of button chosen
	 */
	function updateForm() {
		DOM.$motionOptions.classList.add('hide');
		DOM.$servoOptions.classList.add('hide');
		DOM.$relayOptions.classList.add('hide');
		DOM.$speechOptions.classList.add('hide');
		DOM.$scriptOptions.classList.add('hide');
		DOM.$soundOptions.classList.add('hide');
		DOM.$pauseOptions.classList.add('hide');
		DOM.$servoSequenceOptions.classList.add('hide'); // COMPATIBILITY REASON
		if (document.querySelector('select[name=newNodeTypeChoice]').value !== '') {
			let selectedNodeType = document.querySelector('select[name=newNodeTypeChoice]');
			document.getElementById(selectedNodeType.value + 'Options').classList.remove('hide');
		} else {
			failAlert('Aucune action n\'a été selectionnée !');
		}
	}

	/**
	 * Save the graph on the server
	 */
	function saveGraph() {
		let sequence = graphPanel.getGraph();

		let headers = new Headers();
		headers.append('Content-Type', 'application/json');
		fetch('/save_sequence', {
			method: 'POST',
			headers: headers,
			body: JSON.stringify({seq_name:DOM.$name.value, seq_data:sequence})
		})
			.then((response) => {
				if(response.status != 200) {
					response.json().then((r) => failAlert(r));
					return;
				}
				location.reload();
			});
	}

	/**
	 * Edit the specified sequence
	 * @param {string} seq_name the name of the sequence to edit
	 */
	function editSequence(seq_name) {
		DOM.$name.value = seq_name;
		let sequenceData = document.getElementById('data_' + seq_name).innerHTML;
		let json = JSON.parse(sequenceData);
		graphPanel.updateGraph(json.nodes, json.edges);
	}

	return {
		init: init
	};
})();