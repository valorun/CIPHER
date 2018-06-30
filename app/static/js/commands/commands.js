var editMode=true;
$(document).ready(function() {

    socket.on('update_relay_state', function(relay) {
    	$( "span[value='"+relay.label+"']" ).each(function(){
    		if(relay.state===0){
				$(this).addClass('green');
				$(this).removeClass('dark-red');
    		}
    		else{
    			$(this).addClass('dark-red');
				$(this).removeClass('green');
    		}
    	})
    });

    $("#playSeqButton").on("click", function(){
    	if($("#sequence").val()!==null && $("#sequence").val()!==""){
      		socket.emit('play_sequence', $("#sequence").val());
      	}
    });

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
	updateDraggables();
	updateMode();

  	$(".motion-direction").on("mousedown", function(){
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
	}).on('mouseup', function() { //mouseleave si on veut arreter quand la souris sort du bouton
		var command="motion:0,0";
    	socket.emit('command', command);
	});

	//bouton de changement de mode
	$("#editPanelButton").on("click", updateMode);

	//bouton pour ajouter un bouton
	$("#addButton").on("click", function(){
		var buttonLabel=$("#buttonLabel").val();
		var relay=$("#relays").val();
		//si on a bien sélectionné un nom et un relai
		if(relay===null || buttonLabel===null) return;
		//si le relay selectionné n'est pas déja utilisé
		if(relayAlreadyUsed(relay)){
			alert("Un bouton correspondant au même relai existe déjà");
			return;
		}
		$("#panel").append("<span class='btn dark-red draggable disabled' value="+relay+">"+buttonLabel+"</span>");
		updateDraggables();
	});
});

//test si un bouton corrspondant au relai indiqué existe déja
function relayAlreadyUsed(rel_label){
	var found=false;
	$('.draggable').each(function(){
		if($(this).attr("value")===rel_label){
			found=true;
			return false;
		}
	});
	return found;
}

//met à jour l'apparence d'un bouton
function updateButtonState(relay, state){

}

//met a jour l'affichage suivant le mode (édition ou non)
function updateMode(){
	editMode=!editMode;
	if(editMode){
		$('.draggable').draggable( 'enable' );
		$('.draggable').addClass("disabled");
		$('#editPanelButton').addClass('fa-check');
		$('#editPanelButton').removeClass('fa-edit');
		$('#newButtonOptions').removeClass('hide');
		$('#deleteIcon').removeClass('hide');
	}
	else{
		$('.draggable').draggable( 'disable' );
		$('.draggable').removeClass("disabled");
		$('#editPanelButton').addClass('fa-edit');
		$('#editPanelButton').removeClass('fa-check');
		$('#newButtonOptions').addClass('hide');
		$('#deleteIcon').addClass('hide');
	}
}

//met a jour les boutons, en le attribuant un handler et sauvegardant leur position
function updateDraggables(){
	$('.draggable').each(function(){
		var left=parseInt($(this).attr("left"));
		var top=parseInt($(this).attr("top"));
    	$(this).draggable({
    		stop: function( event, ui ) {
    			var rel_label=$(this).attr("value");
    			if(ui.position.top<20 && ui.position.left<20){ //supprime un objet lorsqu'on l'approche de l'icone de suppression
    				$.post( "/delete_button", {rel_label:rel_label});
    				$(this).remove();
    			}
    			else{
					var btn_label=$(this).text();
					var btn_left=ui.position.left;
					var btn_top=ui.position.top;
					//sauvegarde la position du bouton
					$.post( "/save_button", {rel_label:rel_label, btn_label:btn_label, btn_left:btn_left, btn_top:btn_top});
    			}
  			},
  			grid: [ 20, 20 ],
  			snap: true,
        	containment: $(this).parent()
    	}).on("click",function(){
			if(!editMode){
				command="relay:"+$(this).attr("value");
				console.log(command);
				socket.emit('command', command);
			}
		});
		$(this).css({'top': top, 'left' : left})
	});
	socket.emit('update_relays_state');
}
