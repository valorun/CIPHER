var socket;
var recognition;

var final_transcript = '';
var recognizing = false;


$(document).ready(function() {

	if ('webkitSpeechRecognition' in window) {

		recognition = new webkitSpeechRecognition();

		recognition.continuous = false;
		recognition.interimResults = false;

		recognition.onstart = function() {
			recognizing = true;
		};

		recognition.onerror = function(event) {
			console.log(event.error);
		};

		recognition.onend = function() {
			recognizing = false;
		};

		recognition.onresult = function(event) {
			for (var i = event.resultIndex; i < event.results.length; ++i) {
				if (event.results[i].isFinal) {
					final_transcript += event.results[i][0].transcript;
				}
			}
			final_transcript = capitalize(final_transcript);
			$("#detectionResult").append("<li>"+linebreak(final_transcript)+"</li>");
			socket.emit('speech_detected', final_transcript);
		};
	}
	else{
		alertModal("Ce navigateur n'est pas compatible avec l\'API Webspeech.");
	}
});

var two_line = /\n\n/g;
var one_line = /\n/g;
function linebreak(s) {
	return s.replace(two_line, '<p/>').replace(one_line, '<br>');
}

function capitalize(s) {
	return s.replace(s.substr(0,1), function(m) { return m.toUpperCase(); });
}

function startDictation() {
	if (recognizing) {
		recognition.stop();
		return;
	}
	final_transcript = '';
	recognition.lang = 'fr-FR';
	recognition.start();
}
