var socket;
$(document).ready(function() {
	socket = io.connect('http://192.168.1.20:5000/client');
	socket.on('command', function(msg) {
    	console.log('Message from server: ', msg);
    });
  	socket.on('connect', function() {
    	socket.emit('client_connect');
  	});
});