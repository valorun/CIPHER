$(document).ready(function() {

	$( function() {
		$( "#motion_slider" ).slider({
			orientation: "vertical",
			range: "min",
			min: 0,
			max: 2047,
			value: 0,
			slide: function( event, ui ) {
				$( "#amount" ).val( ui.value );
			}
		});
	});
	

	//selects different listeners depending on the type of device used.
	let startActionEvent = "mousedown";
	let stopActionEvent = "mouseup"; //mouseleave if we also want to stop when the cursor is out of the button
	if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
 		startActionEvent = "touchstart";
 		stopActionEvent = "touchend";
	}

	//carriage controller
	$(".motion-direction").on(startActionEvent, function(){
		var dir=$(this).attr('value');
		var value=$( "#motion_slider" ).slider( "value" );
		var command="motion:";
		if(dir=="motion_up"){
			command+=value+","+value;
		}
		else if(dir=="motion_down"){
			command+="-"+value+",-"+value;
		}
		else if(dir=="motion_left"){
			command+="-"+value+","+value;
		}
		else if(dir=="motion_right"){
			command+=value+",-"+value;
		}
		socket.emit('command', command);
	}).on(stopActionEvent, function() {
		var command="motion:0,0";
		socket.emit('command', command);
	});
});