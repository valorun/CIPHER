var socket;
$(document).ready(function() {
	socket = io.connect('http://127.0.0.1:5000/client');
	socket.on('command', function(msg) {
    	console.log('Message from server: ', msg);
    });
  	socket.on('connect', function() {
    	socket.emit('client_connect');
  	});
});
