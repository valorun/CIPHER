/* globals fetchJson */

/* exported relaysSettingsController */
const relaysSettingsController = (() => {
	'use strict';

	const DOM = {};

	/* PUBLIC METHODS */
	function init() {
		cacheDom();
		bindUIEvents();
	}

	/* PRIVATE METHODS */
	function bindUIEvents() {
		document.getElementById('addRelay').addEventListener('click', () => {

			fetchJson('/save_relay', 'POST', 
				{rel_label: DOM.$newRelayLabel.value,
					rel_pin: DOM.$newRelayPin.value,
					rel_parity: DOM.$newRelayParity.value,
					raspi_id: DOM.$newRelayRaspiId.value})
				.then(() => {
					location.reload();
				});
		});

		// checkbox to enable or disable the relay
		document.querySelectorAll('input[name=enableRel]').forEach(e => {
			const rel_label = e.id.substring(e.id.indexOf('_') + 1);
			e.addEventListener('change', () => {
				enableRelay(rel_label, e.checked);
			});
		});

		// button to delete the relay
		document.querySelectorAll('a[name=deleteRel]').forEach(e => {
			const rel_label = e.id.substring(e.id.indexOf('_') + 1);
			e.addEventListener('click', () => {
				deleteRelay(rel_label);
			});
		});
	}

	function cacheDom() {
		DOM.$newRelayLabel = document.getElementById('newRelayLabel');
		DOM.$newRelayPin = document.getElementById('newRelayPin');
		DOM.$newRelayParity = document.getElementById('newRelayParity');
		DOM.$newRelayRaspiId = document.getElementById('newRelayRaspiId');

	}

	/**
 	 *  Enable OR disable a relay
	 *	@param	{string} rel_label relay label
	 *	@param	{boolean} value new state for the relay
 	 */
	function enableRelay(rel_label, value) {
		fetchJson('/enable_relay', 'POST', {rel_label: rel_label, value: value})
			.then(() => {
				console.log(rel_label + ' updated');
			});
	}

	/**
 	 *  Delete a relay
 	 *	@param	{string} rel_label relay label
 	 */
	function deleteRelay(rel_label) {
		const confirm = window.confirm('Etes vous sûr de vouloir supprimer le relai \'' + rel_label + '\' ?');
		if (confirm) {
			fetchJson('/delete_relay', 'POST', {rel_label: rel_label})
				.then(() => {
					console.log(rel_label + ' deleted');
					const el = document.getElementById(rel_label);
					el.parentNode.removeChild(el);
				});
		}
	}

	return {
		init: init
	};
})();
