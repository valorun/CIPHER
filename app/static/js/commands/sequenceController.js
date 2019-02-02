var sequenceController = {
	init: function(){
		this.bind();
	},
	bind: function(){
		//directly play a sequence in the list
		$("#playSeqButton").on("click", () => {
			if($("#sequence").val()!==null && $("#sequence").val()!==""){
				socket.emit('play_sequence', $("#sequence").val());
			}
		});
	}
}
