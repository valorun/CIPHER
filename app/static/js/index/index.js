$(document).ready(function() {

    $("#shutdownButton").on("click", function(){
    	socket.emit("shutdown");
    });
    $("#rebootButton").on("click", function(){
    	socket.emit("reboot");
    });
});