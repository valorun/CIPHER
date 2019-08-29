var debugController = (() => {
	'use strict';

	let DOM = {};

	/* PUBLIC METHODS */
	function init(){
		cacheDom();
		bindUIEvents();
	}

	/* PRIVATE METHODS */
	function bindUIEvents(){
		document.getElementById('sendStatementButton').addEventListener('click', () =>{
			socket.emit('speech_detected', DOM.$statement.value);
		});
	}
	
	function cacheDom() {
		DOM.$statement = document.getElementById('statement');
	}

	return {
		init: init
	}
})();