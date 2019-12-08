/* globals fetchJson */

/* exported servosSettingsController */
const servosSettingsController = (() => {
	'use strict';

	const DOM = {};

	/* PUBLIC METHODS */
	function init() {
		cacheDom();
		bindUIEvents();
	}

	/* PRIVATE METHODS */
	function bindUIEvents() {
		document.getElementById('addServo').addEventListener('click', () => {

			fetchJson('/save_servo', 'POST', 
				{ servo_label: DOM.$newServoLabel.value,
					servo_pin: DOM.$newServoPin.value,
					min_pulse_width: DOM.$newServoMinPulseWidth.value,
					max_pulse_width: DOM.$newServoMaxPulseWidth.value,
					def_pulse_width: DOM.$newServoDefPulseWidth.value,
					raspi_id: DOM.$newServoRaspiId.value })
				.then(() => {
					location.reload();
				});
		});

		// checkbox to enable or disable the servo
		document.querySelectorAll('input[name=enableServo]').forEach(e => {
			const servo_label = e.id.substring(e.id.indexOf('_') + 1);
			e.addEventListener('change', () => {
				enableServo(servo_label, e.checked);
			});
		});

		// button to delete the servo
		document.querySelectorAll('a[name=deleteServo]').forEach(e => {
			const servo_label = e.id.substring(e.id.indexOf('_') + 1);
			e.addEventListener('click', () => {
				deleteServo(servo_label);
			});
		});
	}

	function cacheDom() {
		DOM.$newServoLabel = document.getElementById('newServoLabel');
		DOM.$newServoPin = document.getElementById('newServoPin');
		DOM.$newServoMinPulseWidth = document.getElementById('newServoMinPulseWidth');
		DOM.$newServoMaxPulseWidth = document.getElementById('newServoMaxPulseWidth');
		DOM.$newServoDefPulseWidth = document.getElementById('newServoDefPulseWidth');
		DOM.$newServoRaspiId = document.getElementById('newServoRaspiId');
	}

	/**
 	 *  Enable OR disable a servo
	 *	@param	{string} servo_label servo label
	 *	@param	{boolean} value new state for the servo
 	 */
	function enableServo(servo_label, value) {
		fetchJson('/enable_servo', 'POST', { servo_label: servo_label, value: value })
			.then(() => {
				console.log(servo_label + ' updated');
			});
	}

	/**
 	 *  Delete a servo
 	 *	@param	{string} servo_label relay label
 	 */
	function deleteServo(servo_label) {
		const confirm = window.confirm('Etes vous sûr de vouloir supprimer le servomoteur \'' + servo_label + '\' ?');
		if (confirm) {
			fetchJson('/delete_servo', 'POST', { servo_label: servo_label })
				.then(() => {
					console.log(servo_label + ' deleted');
					const el = document.getElementById(servo_label);
					el.parentNode.removeChild(el);
				});
		}
	}

	return {
		init: init
	};
})();
