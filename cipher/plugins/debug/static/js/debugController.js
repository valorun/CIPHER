var debugController = {
	init: function(){
		this.bind();
	},
	bind: function(){
		$("#sendStatementButton").on("click", function(){
			socket.emit('speech_detected', $("#statement").val());
		});
	}

}
