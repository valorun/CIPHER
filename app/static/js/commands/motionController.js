var motionController = {
	wheelsMode: false, //set to true if the robot is on wheels
	init: function() {
		$.ajax({
			type: 'POST',
			url: '/get_motion_mode',
			success: (data) =>{
				this.wheelsMode = data;
				this.bind();
			},
			error: (request, status, error) =>{
				failAlert(request.responseText);
			}
		});
	},
	bind: function() {
		$( "#motion_slider" ).slider({
			orientation: "vertical",
			range: "min",
			min: 0,
			max: 2047,
			value: 0,
			slide: ( event, ui ) => {
				$( "#amount" ).val( ui.value );
			}
		});

		//selects different listeners depending on the type of device used.
		let startActionEvent = "mousedown";
		let stopActionEvent = "mouseup"; //mouseleave if we also want to stop when the cursor is out of the button
		if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
 			startActionEvent = "touchstart";
 			stopActionEvent = "touchend";
		}

		//carriage controller
		$(".motion-direction").on(startActionEvent, (e) => {
			var dir=$(e.currentTarget).attr('value');
			var value=$( "#motion_slider" ).slider( "value" );
			var command="motion:";
			if(dir=="motion_up"){
				command+=value+","+value;
			}
			else if(dir=="motion_down"){
				command+="-"+value+",-"+value;
			}
			else if(dir=="motion_left"){
				if (this.wheelsMode)
					command+="0,"+value;
				else
					command+="-"+value+","+value;
			}
			else if(dir=="motion_right"){
				if (this.wheelsMode)
					command+=value+",0";
				else
					command+=value+",-"+value;
			}
			console.log(command);
			socket.emit('command', command);
		}).on(stopActionEvent, () => {
			var command="motion:0,0";
			socket.emit('command', command);
		});
	}
}