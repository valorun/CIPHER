$(document).ready(function() {

	//directly play a sequence in the list
	$("#playSeqButton").on("click", function(){
		if($("#sequence").val()!==null && $("#sequence").val()!==""){
			socket.emit('play_sequence', $("#sequence").val());
		}
	});

});
