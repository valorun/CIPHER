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
			let dir=$(e.currentTarget).attr('value');
			let value=$( "#motion_slider" ).slider( "value" );
			let left = 0;
			let right = 0;
			if(dir=="motion_up"){
				left = value;
				right = value;
			}
			else if(dir=="motion_down"){
				left = -value;
				right = -value
			}
			else if(dir=="motion_left"){
				if (this.wheelsMode)
					right = value;
				else{
					left = -value;
					right = value;
				}
			}
			else if(dir=="motion_right"){
				if (this.wheelsMode)
					left = value;
				else{
					left = value;
					right = -value;
				}
			}
			console.log(left + ", " + right);
			socket.emit('move', left, right);
		}).on(stopActionEvent, () => {
			console.log("0, 0");
			socket.emit('move', 0, 0);
		});
	}
}