var dictationController = {
	recognition: null,
	final_transcript: '',
	recognizing: false,

	init: function(){
		if (!('webkitSpeechRecognition' in window)){
			failAlert("Ce navigateur n'est pas compatible avec l\'API Webspeech.");
			return;
		}

		this.recognition = new webkitSpeechRecognition();
		this.recognition.continuous = false;
		this.recognition.interimResults = false;

		this.bind();
	},
	bind: function(){
		this.recognition.onstart = () => {
			this.recognizing = true;
		};

		this.recognition.onerror = (event) => {
			console.log(event.error);
		};

		this.recognition.onend = () => {
			this.recognizing = false;
		};

		this.recognition.onresult = (event) => {
			for (let i = event.resultIndex; i < event.results.length; ++i) {
				if (event.results[i].isFinal) {
					this.final_transcript += event.results[i][0].transcript;
				}
			}
			this.final_transcript = linebreak(capitalize(this.final_transcript));
			let time = new Date();
			$("#detectionResult").append("<li>"+
											"<div class='row'>"+
												"<div class='container round-large pale-green border col l10 m10 s9'>" +
													"<div class='right-align'><p>" +
														this.final_transcript +
													"</p></div>"+
													"<div class='left-align'><p>" + time.getHours() + ":" + time.getMinutes() + "</p></div>" +
												"</div>" +
												"<div class='col l2 m2 s3 center'>" +
													"<span class='border circle large btn hover-none'><i class='fas fa-microphone fa-fw'></i></span>" +
												"</div>" +
											"</div>" +
										"</li>");
			$("#detectionResult").parent().scrollTop($("#detectionResult").parent().height());
			socket.emit('speech_detected', this.final_transcript);
		};

		//server response when a sentence must be play on the client
		socket.on('response', (msg) => {
			let time = new Date();
			$("#detectionResult").append("<li>"+
											"<div class='row'>"+
												"<div class='col l2 m2 s3 center'>" +
													"<span class='border circle large btn hover-none'><i class='fas fa-robot fa-fw'></i></span>" +
												"</div>" +
												"<div class='container round-large light-grey border col l10 m10 s9'>" +
													"<div class='left-align'><p>" +
														msg +
													"</p></div>"+
													"<div class='right-align'><p>" + time.getHours() + ":" + time.getMinutes() + "</p></div>" +
												"</div>" +
											"</div>" +
										"</li>");
			$("#detectionResult").parent().scrollTop($("#detectionResult").parent().height());
		});
	},
	startDictation: function() {
		//console.log(this);
		if (this.recognizing) {
			this.recognition.stop();
			return;
		}
		this.final_transcript = '';
		this.recognition.lang = 'fr-FR';
		this.recognition.start();
	}
}
