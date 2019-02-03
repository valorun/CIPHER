var raspiesController = {
	init: function(){
		this.bind();
		socket.emit("get_raspies");
	},
	bind: function(){
		$("#shutdownButton").on("click", () => {
    		socket.emit("shutdown");
    	});
    	$("#rebootButton").on("click", () => {
    		socket.emit("reboot");
    	});
    	socket.on('get_raspies', (raspies) => {
			console.log(raspies);
    		this.updateRaspies(raspies);
    	});

	},

	updateRaspies: function(raspies){
		$("#raspberries").empty();
		$.each(raspies, function(i, raspi){
			console.log(raspi);
			let card = "<div class='container cell pale-green topbar bottombar border-green margin-left'>"+
					"<h3>"+ raspi.id + " | " + raspi.address+"</h3>"+
				"</div>";
			$("#raspberries").append(card);
		});

	}
}
