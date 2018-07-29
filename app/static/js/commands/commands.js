var editMode=true;
$(document).ready(function() {

	//initialise les positions des boutons
	var panel_width=$("#panel").width();
	var panel_height=$("#panel").height();
	$('.draggable').each(function(){
		var left=parseFloat($(this).attr("left"))*panel_width;
		var top=parseFloat($(this).attr("top"))*panel_height;
		$(this).attr("left", left);
		$(this).attr("top", top);
	});

	function rescale_panel(){
		var new_panel_width=$("#panel").width();
		var new_panel_height=$("#panel").height();
		$('.draggable').each(function(){
			var left=parseFloat($(this).attr("left"))/panel_width*new_panel_width;
			var top=parseFloat($(this).attr("top"))/panel_height*new_panel_height;
			left=Math.abs(left);
			top=Math.abs(top);
			$(this).attr("left", left);
			$(this).attr("top", top);
		});
		panel_width=new_panel_width;
		panel_height=new_panel_height;
	}

	$(window).bind('resize', function(e){
		rescale_panel();
		updateDraggables();
	});


	socket.on('updateRelayState', function(relay) {
		$( "span[value='"+relay.label+"']" ).each(function(){
			if(relay.state===1){
				$(this).addClass('green');
				$(this).removeClass('dark-red');
			}
			else if(relay.state===0){
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

	//bouton de changement de mode
	$("#editPanelButton").on("click", updateMode);

	//bouton pour ajouter un bouton
	$("#addButton").on("click", function(){
		var buttonLabel=$("#buttonLabel").val();
		var relay=$("#relays").val();
		//si le relay selectionné n'est pas déja utilisé
		if(relayAlreadyUsed(relay)){
			alertModal("Un bouton correspondant au même relai existe déjà.");
			return;
		}
		console.log(relay);
		$.ajax({
			type: 'POST',
			url: '/save_button',
			data: {rel_label:relay, btn_label:buttonLabel, btn_left:"0.0", btn_top:"0.0"},
			success: function(){
				$("#panel").append("<span class='btn draggable disabled' value="+relay+">"+buttonLabel+"</span>");
				updateDraggables();
			},
			error: function(request, status, error){
				alertModal(request.responseText);
			}
		});
	});
});

//test si un bouton correspondant au relai indiqué existe déja
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
	var panel_width=$("#panel").width();
	var panel_height=$("#panel").height();
	$('.draggable').each(function(){
		var left=parseInt($(this).attr("left")); //position précédemment définie
		var top=parseInt($(this).attr("top"));
		$(this).draggable({
			stop: function( event, ui ) {
				var rel_label=$(this).attr("value");
    			if(ui.position.top<20 && ui.position.left<20){ //supprime un objet lorsqu'on l'approche de l'icone de suppression
    				var btn=$(this);
    			$.ajax({
    				type: 'POST',
    				url: '/delete_button',
    				data: {rel_label:rel_label},
    				success: function(){
    					btn.remove();
    				},
    				error: function(request, status, error){
    					alertModal(request.responseText);
    				}
    			});
    		}
    		else{
    			var btn_label=$(this).text();
    			var btn_left=ui.position.left;
    			var btn_top=ui.position.top;
    				$(this).attr("left", btn_left); //on garde la nouvelle position
    				$(this).attr("top", btn_top);
					//sauvegarde la position du bouton
					$.ajax({
						type: 'POST',
						url: '/save_button',
						data: {rel_label:rel_label, btn_label:btn_label, btn_left:btn_left/panel_width, btn_top:btn_top/panel_height},
						success: function(){

						},
						error: function(request, status, error){
							alertModal(request.responseText);
						}
					});
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
		$(this).css({'top': top, 'left' : left})//on applique la position précédemment définie
	});

	socket.emit('update_relays_state');
}
