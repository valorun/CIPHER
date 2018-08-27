var socket = io.connect(window.location.host+'/client');

var connectionManager = {
	voices: null,
	init: function(){
		window.speechSynthesis.onvoiceschanged = () => {
			this.voices=window.speechSynthesis.getVoices();
		}

		this.bind();
	},
	bind: function(){
		socket.on('command', function(msg) {
			console.log('Message from server: ', msg);
		});

		//server response when a sentence must be play on the client
		socket.on('response', (msg) => {
			console.log('Message from server:', msg);
			this.speak(msg);
		});
		socket.on('play_sound', function(sound_name) {
			var audio = new Audio(window.location.origin+'/play_sound/'+sound_name);
			audio.play();
		});
	},

	speak: function(msg){
		if ('speechSynthesis' in window) {
			let to_speak = new SpeechSynthesisUtterance(msg);
			$.each(this.voices,function(){
				if(Cookies.get("voice") === this.name){
					to_speak.voice = this;
				}
			});
			window.speechSynthesis.speak(to_speak);
		}
	}
}
