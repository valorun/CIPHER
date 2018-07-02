var socket;
$(document).ready(function() {
	socket = io.connect('https://192.168.1.78:5000/client');
	socket.on('command', function(msg) {
    	console.log('Message from server: ', msg);
    });
  	socket.on('connect', function() {
    	socket.emit('client_connect');
  	});
});
