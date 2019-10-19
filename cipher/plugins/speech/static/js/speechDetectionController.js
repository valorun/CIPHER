/* globals socket */

/* exported speechDetectionController */
var speechDetectionController = (() => {
	'use strict';

	let DOM = {};

	/* PUBLIC METHODS */
	function init() {
		cacheDom();
		bindUIEvents();
	}

	/* PRIVATE METHODS */
	function bindUIEvents(){

		DOM.$startRecognition.addEventListener('click', () => {
			DOM.$speechDetectionModal.style.display = 'block';
		});

		DOM.$stopRecognition.addEventListener('click', () => {
			DOM.$speechDetectionModal.style.display = 'none';
		});
		
		//server response when a sentence must be play on the client
		socket.on('response', (msg) => {
			let time = new Date();
			DOM.$detectionResult.insertAdjacentHTML('beforeend', '<li>'+
					'<div class="row">'+
						'<div class="col l2 m2 s3 center">' +
							'<span class="border circle large btn hover-none"><i class="fas fa-robot fa-fw"></i></span>' +
						'</div>' +
						'<div class="container round-large light-grey border col l10 m10 s9">' +
							'<div class="left-align"><p>' +
								msg +
							'</p></div>'+
							'<div class="right-align"><p>' + time.getHours() + ':' + time.getMinutes() + '</p></div>' +
						'</div>' +
					'</div>' +
				'</li>');
			DOM.$detectionResult.parentElement.scrollTop = DOM.$detectionResult.parentElement.offsetHeight;
		});

	}

	function cacheDom() {
		DOM.$startRecognition = document.getElementById('startRecognition');
		DOM.$stopRecognition = document.getElementById('stopRecognition');
		DOM.$speechDetectionModal = document.getElementById('speechDetectionModal');
		DOM.$detectionResult = document.getElementById('detectionResult');

	}

	return {
		init: init
	};
})();
