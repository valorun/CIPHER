/* globals ace */
/* globals templateController */
/* globals fetchJson */

/* exported editorController */
const editorController = (() => {
	'use strict';

	const DOM = {};
	let editor = null;

	/* PUBLIC METHODS */
	function init(){
		editor = ace.edit('editor', {
			theme: 'ace/theme/twilight',
			mode: 'ace/mode/python',
			selectionStyle: 'text'
		});
		cacheDom();
		bindUIEvents();
	}

	/* PRIVATE METHODS */
	function bindUIEvents() {
		document.querySelectorAll('a[name=editScript]').forEach((e) => {
			const script_name = e.id.substring(e.id.indexOf('_') + 1);
			e.addEventListener('click', () => {
				editScript(script_name);
			});
		});

		document.querySelectorAll('a[name=deleteScript]').forEach((e) => {
			const script_name = e.id.substring(e.id.indexOf('_') + 1);
			e.addEventListener('click', () => {
				deleteScript(script_name);
			});
		});
		
		document.getElementById('saveButton').addEventListener('click', () => {
			saveScript(DOM.$scriptName.value, editor.getValue());
		});
	}

	function cacheDom() {
		DOM.$scriptName = document.getElementById('name');
	}

	/**
	 * Edit the specified script
	 * @param {string} script_name the name of the script to edit
	 */
	function editScript(script_name) {
		DOM.$scriptName.value = script_name;

		fetchJson('/read_script/' + script_name, 'GET')
			.then(data => {
				editor.setValue(data);
				templateController.getAccordion('editorPanel').open();
				window.location.hash = '#editorPanel';
			});
	}

	/**
	 * Completely delete a script
	 * @param {string} script_name the name of the script to delete
	 */
	function deleteScript(script_name){
		const confirm = window.confirm('Etes vous sûr de vouloir supprimer le script \'' + script_name + '\' ?');
		if(confirm){
			fetchJson('/delete_script', 'POST', {script_name:script_name})
				.then(()=> {
					console.log(script_name + ' deleted');
					DOM.$scriptName.remove();
					location.reload();
				});
		}
	}

	/**
	 * Save a script on the server
	 * @param {string} script_name the name of the script to save
	 * @param {string} script_data the data of the script to save
	 */
	function saveScript(script_name, script_data) {
		fetchJson('/save_script', 'POST', {script_name:script_name, script_data:script_data})
			.then(() => {
				console.log(script_name + ' saved');
				location.reload();
			});
	}

	return {
		init: init
	};

})();