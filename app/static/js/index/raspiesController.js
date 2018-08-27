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
    		this.updateRaspies(raspies);
    	});

	},

	updateRaspies: function(raspies){
		$("#raspberries").empty();
		$.each(raspies, function(i, raspi){
			console.log(raspi);
			let action = "<h4>Modes: </h4>";
			let valid = "<i class='fa fa-check-circle green circle large'></i> </p>";
			let invalid = "<i class='fa fa-times-circle dark-red circle large'></i> </p>";
			if(raspi.motion_mode)
				action += "<p>MOTION "+valid;
			else
				action += "<p>MOTION "+invalid;
			if(raspi.relay_mode)
				action += "<p>RELAY "+valid;
			else
				action += "<p>RELAY "+invalid;
			if(raspi.servo_mode)
				action += "<p>SERVO "+valid;
			else
				action += "<p>SERVO "+invalid;

			let card = "<div class='container cell pale-green topbar bottombar border-green'>"+
					"<h3>"+ raspi.id + " | " + raspi.address+"</h3>"+
					"<p>"+raspi.sid+"</p>"+
					"<p>"+action+"</p>"+
				"</div>";
			$("#raspberries").append(card);
		});

	}
}
