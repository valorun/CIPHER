var socket = io.connect(window.location.host+'/client');

var connectionManager = {
	voices: null,
	audio: null,
	init: function(){
		window.speechSynthesis.onvoiceschanged = () => {
			this.voices=window.speechSynthesis.getVoices();
		}
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
				this.audio = new Audio(window.location.origin+'/play_sound/'+sound_name);
				this.audio.play();
			}
		});
		socket.on('connect', () => {
			$("#socketErrorModal").hide()
		});
		socket.on('disconnect', () => {
			$("#socketErrorModal").show()
		});
	},

	speak: function(msg){
		if ('speechSynthesis' in window) {
			let to_speak = new SpeechSynthesisUtterance(msg);
			$.each(this.voices, (i, e) =>{
				if(Cookies.get("voice") === e.name){
					to_speak.voice = e;
				}
			});
			window.speechSynthesis.speak(to_speak);
		}
	}
}
