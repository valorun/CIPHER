/* globals socket */

/* exported raspiesController */
const raspiesController = (() => {
	'use strict';
	const DOM = {};

	/* PUBLIC METHODS */
	function init() {
		cacheDom();
		bindUIEvents();
		bindSocketIOEvents();
		socket.emit('get_raspies');
	}
	
	/* PRIVATE METHODS */
	function bindUIEvents(){
		document.getElementById('shutdownButton').addEventListener('click', () => {
			socket.emit('shutdown');
		});
		document.getElementById('rebootButton').addEventListener('click', () => {
			socket.emit('reboot');
		});
	}

	function bindSocketIOEvents() {
		socket.on('get_raspies', (raspies) => {
			updateRaspies(raspies);
		});
	}

	function cacheDom() {
		DOM.$raspberries = document.getElementById('raspberries');
	}

	function updateRaspies(raspies) {
		// first empty the container ...
		DOM.$raspberries.innerHTML = '';

		// then add all current raspies
		raspies.forEach(raspi => {
			console.log(raspi);
			const card = '<div class=\'container cell center pale-green round-large border border-green padding-16\''+
							'<h3><strong><i class=\'xxxlarge fab fa-raspberry-pi\'></i></strong></h3>' +
							'<h3>' + raspi.id + '</h3>' +
						'</div>';
			DOM.$raspberries.insertAdjacentHTML('beforeend', card);
		});
	}

	return {
		init: init
	};
})();
