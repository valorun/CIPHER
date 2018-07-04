var socket;
$(document).ready(function() {
	socket = io.connect('https://192.168.1.78:5000/client');
	socket.on('command', function(msg) {
    		console.log('Message from server: ', msg);
   	 });
  	socket.on('connect', function() {
    		socket.emit('client_connect');
  	});
	//reponse du serveur lors d'une de l'  coute d'une phrase
  	socket.on('response', function(msg) {
    		console.log('Message from server: ', msg);
    		if ('speechSynthesis' in window) {
      			var to_speak = new SpeechSynthesisUtterance(msg);
      			window.speechSynthesis.speak(to_speak);
    		}
  	});

});
