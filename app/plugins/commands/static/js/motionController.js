var motionController = {
	init: function() {
		this.bind();
	},
	bind: function() {
		$( "#motion_slider" ).slider({
			orientation: "vertical",
			range: "min",
			min: 0,
			max: 100,
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
			let direction=$(e.currentTarget).attr('value').split('_')[1];
			let speed=$( "#motion_speed" ).slider( "value" );
			
			console.log(direction + ", " + speed);
			socket.emit('move', direction, speed);
		}).on(stopActionEvent, () => {
			console.log("stop, 0");
			socket.emit('move', "stop", 0);
		});
	}
}