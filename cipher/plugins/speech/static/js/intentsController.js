/* globals failAlert */

/* exported intentsController */
var intentsController = (() => {
	'use strict';

	let DOM = {};

	/* PUBLIC METHODS */
	function init() {
		cacheDom();
		bindUIEvents();
	}

	/* PRIVATE METHODS */
	function bindUIEvents(){
		//button to add the sentence to the conversation
		document.getElementById('addResponseButton').addEventListener('click', () => {
			let intent = DOM.$currentIntent.value;
			if(intent == null || intent === ''){
				failAlert('L\'intention fournie est vide.');
				return;
			}
			let script_name = DOM.$currentScriptName.value;
			let sequence_id = DOM.$currentSequence.value;
			saveIntent(intent, script_name, sequence_id);
		});

		//checkbox to enable or disable the relay
		document.querySelectorAll('input[name=enableIntent]').forEach((e) => {
			const intent = e.id.substr(e.id.indexOf('_') + 1);
			e.addEventListener('change', () => {
				enableIntent(intent, e.checked);
			});
		});

		//button to delete the relay
		document.querySelectorAll('a[name=deleteIntent]').forEach((e) => {
			const intent = e.id.substr(e.id.indexOf('_') + 1);
			e.addEventListener('click', () => {
				deleteIntent(intent);
			});
		});
	}

	function cacheDom() {
		DOM.$currentIntent = document.getElementById('currentIntent');
		DOM.$currentScriptName = document.getElementById('currentScriptName');
		DOM.$currentSequence = document.getElementById('currentSequence');
	}

	/**
	 * Save an intent
	 * @param {*} intent intant name
	 * @param {*} script_name optional script name
	 * @param {*} sequence_id optional sequence id
	 */
	function saveIntent(intent, script_name, sequence_id) {
		let headers = new Headers();
		headers.append('Content-Type', 'application/json');
		fetch('/save_intent', {
			method: 'POST',
			headers: headers,
			body: JSON.stringify({intent: intent, script_name: script_name, sequence_id: sequence_id})
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
 	 *  Enable OR disable an intent
	  *	@param	{string} intent intant name
	  *	@param	{boolean} value new state for the intent
 	 */
	function enableIntent(intent, value) {
		let headers = new Headers();
		headers.append('Content-Type', 'application/json');
		fetch('/enable_intent', {
			method: 'POST',
			headers: headers,
			body: JSON.stringify({intent:intent, value:value})
		})
			.then((response) => {
				if(response.status != 200) {
					response.json().then((r) => failAlert(r));
					return;
				}
				console.log(intent + ' updated');

			});
	}

	/**
 	 *  Delete an intent
 	 *	@param	{string} intent intent name
 	 */
	function deleteIntent(intent) {
		var confirm = window.confirm('Etes vous sûr de vouloir supprimer l\'intention \'' + intent + '\' ?');
		let headers = new Headers();
		headers.append('Content-Type', 'application/json');
		if (confirm) {
			fetch('/delete_intent', {
				method: 'POST',
				headers: headers,
				body: JSON.stringify({intent:intent})
			})
				.then((response) => {
					if(response.status != 200) {
						response.json().then((r) => failAlert(r));
						return;
					}
					console.log(intent + ' deleted');
					let intent_el = document.getElementById(intent);
					intent_el.parentNode.removeChild(intent_el);
				});
		}
	}

	return {
		init: init
	};
})();
