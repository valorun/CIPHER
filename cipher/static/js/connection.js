var socket = io.connect(window.location.host + '/client');

var connectionManager = {
	voices: null,
	audio: null,
	init: function(){
		this.voices = window.speechSynthesis.getVoices();

		window.speechSynthesis.onvoiceschanged = () => {
			this.voices = window.speechSynthesis.getVoices();
		};
		this.bind();
	},
	bind: function(){
		socket.on('command', (msg) => {
			console.log('Message from server: ', msg);
		});

		//server response when a sentence must be play on the client
		socket.on('response', (msg) => {
			console.log('Message from server: ', msg);
			this.speak(msg);
		});
		socket.on('play_sound', (sound_name) => {
			if(this.audio != null ){
				this.audio.pause();
				this.audio = null;
			}
			else {
				this.audio = new Audio(window.location.origin + '/play_sound/' + sound_name);
				this.audio.play();
			}
		});
		socket.on('connect', () => {
			document.getElementById('socketErrorModal').style.display = 'none';
		});
		socket.on('disconnect', () => {
			document.getElementById('socketErrorModal').style.display = 'block';
		});
	},

	speak: function(msg){
		if ('speechSynthesis' in window && this.voices !== null) {
			let to_speak = new SpeechSynthesisUtterance(msg);
			this.voices.forEach((e) =>{
				if(Cookies.get('voice') === e.name){
					to_speak.voice = e;
				}
			});
			window.speechSynthesis.speak(to_speak);
		}
	}
};
