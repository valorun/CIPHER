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
	
	//controles du chariot
	$(".motion-direction").on("mousedown touchstart", function(){
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
	}).on('mouseup touchend', function() { //mouseleave si on veut arreter quand la souris sort du bouton
		var command="motion:0,0";
		socket.emit('command', command);
	});
});