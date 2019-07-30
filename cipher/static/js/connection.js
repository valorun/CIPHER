var socket = io.connect(window.location.host + '/client');

var connectionManager = (() => {
	'use strict';

	let voices = null;
	let audio = null;

	/* PUBLIC METHODS */
	function init(){
		voices = window.speechSynthesis.getVoices();

		window.speechSynthesis.onvoiceschanged = () => {
			voices = window.speechSynthesis.getVoices();
		};
		bindSocketIOEvents();
	}

	function speak(msg) {
		if ('speechSynthesis' in window && voices !== null) {
			let to_speak = new SpeechSynthesisUtterance(msg);
			voices.forEach((e) =>{
				if(Cookies.get('voice') === e.name){
					to_speak.voice = e;
				}
			});
			window.speechSynthesis.speak(to_speak);
		}
	}

	/* PRIVATE METHODS */
	function bindSocketIOEvents(){
		socket.on('command', (msg) => {
			console.log('Message from server: ', msg);
		});

		//server response when a sentence must be play on the client
		socket.on('response', (msg) => {
			console.log('Message from server: ', msg);
			speak(msg);
		});
		socket.on('play_sound', (sound_name) => {
			if(audio != null ){
				audio.pause();
				audio = null;
			}
			else {
				audio = new Audio(window.location.origin + '/play_sound/' + sound_name);
				audio.play();
			}
		});
		socket.on('connect', () => {
			document.getElementById('socketErrorModal').style.display = 'none';
		});
		socket.on('disconnect', () => {
			document.getElementById('socketErrorModal').style.display = 'block';
		});
	}

	return {
		init: init,
		speak: speak
	};
})();
