/* globals failAlert */
/* globals fetchJson */

/* exported intentsController */
const intentsController = (() => {
	'use strict';

	const DOM = {};

	/* PUBLIC METHODS */
	function init() {
		cacheDom();
		bindUIEvents();
	}

	/* PRIVATE METHODS */
	function bindUIEvents(){
		//button to add the sentence to the conversation
		document.getElementById('addResponseButton').addEventListener('click', () => {
			const intent = DOM.$currentIntent.value;
			if(intent == null || intent === ''){
				failAlert('L\'intention fournie est vide.');
				return;
			}
			const script_name = DOM.$currentScriptName.value;
			const sequence_id = DOM.$currentSequence.value;
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
		fetchJson('/save_intent', 'POST', 
			{intent: intent, script_name: script_name, sequence_id: sequence_id})
			.then(() => {
				location.reload();
			});
	}

	/**
 	 *  Enable OR disable an intent
	  *	@param	{string} intent intant name
	  *	@param	{boolean} value new state for the intent
 	 */
	function enableIntent(intent, value) {
		fetchJson('/enable_intent', 'POST', {intent:intent, value:value})
			.then(() => {
				console.log(intent + ' updated');
			});
	}

	/**
 	 *  Delete an intent
 	 *	@param	{string} intent intent name
 	 */
	function deleteIntent(intent) {
		const confirm = window.confirm('Etes vous sûr de vouloir supprimer l\'intention \'' + intent + '\' ?');
		
		if (confirm) {
			fetchJson('/delete_intent', 'POST', {intent:intent})
				.then(() => {
					console.log(intent + ' deleted');
					const intent_el = document.getElementById(intent);
					intent_el.parentNode.removeChild(intent_el);
				});
		}
	}

	return {
		init: init
	};
})();
