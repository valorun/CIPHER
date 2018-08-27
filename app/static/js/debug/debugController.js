var debugController = {
	init: function(){
		this.bind();
	},
	bind: function(){
		$("#sendCommandButton").on("click", function(){
			socket.emit('command', $("#command").val());
		});
		$("#sendStatementButton").on("click", function(){
			socket.emit('speech_detected', $("#statement").val());
		});
	}

}
