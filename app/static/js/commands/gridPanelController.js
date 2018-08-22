let gridPanel = null;

$(document).ready(function() {
	gridPanel= new GridPanel($('#grid'), $("#editPanelButton"), $('#newButtonPanel'));

	//initialize the grid at his initial state in disabled edition mode
	loadGrid();

	$("#addButton").on("click", function(){
		var buttonLabel=$("#buttonLabel").val();
		var color=$("#color").data("color");

		var action=null;
		var sequence=null;
		if ($("#relayChoice").prop("checked") == true) {
			action="relay:"+$("#relays").val();
			//if the relay isn't already used
			if(actionAlreadyUsed(action)){
				alertModal("Un bouton correspondant au même relai existe déjà.");
				return;
			}
		} else if ($("#sequenceChoice").prop("checked") == true) {
			sequence=$("#sequences").val();
			if(sequenceAlreadyUsed(sequence)){
				alertModal("Un bouton correspondant à la même sequence existe déjà.");
				return;
			}
		} else if ($("#soundChoice").prop("checked") == true) {
			action="sound:"+$("#sounds").val();
			//if the sound isn't already used
			if(actionAlreadyUsed(action)){
				alertModal("Un bouton correspondant au même son existe déjà.");
				return;
			}
		}
		
		gridPanel.addButton(buttonLabel, action, sequence, color, 1, 1, 1, 1);
	});

	$('input[type=radio][name=choice]').on("change", function() {
		gridPanel.updateForm();
	});

	$("#editPanelButton").on("click", function(){
		gridPanel.updateMode();
		saveGrid();
	});

});

//check if a button with the same action already exists
function actionAlreadyUsed(label){
	var found=false;
	$('.grid-stack-item-content').each(function(){
		if($(this).data("action")===label){
			found=true;
			return false;
		}
	});
	return found;
}

//check if a button with the same sequence already exists
function sequenceAlreadyUsed(label){
	var found=false;
	$('.grid-stack-item-content').each(function(){
		if($(this).data("sequence")===label){
			found=true;
			return false;
		}
	});
	return found;
}

//load the grid from the server
function loadGrid() {
	gridPanel.clearGrid();
	$.ajax({
		type: 'POST',
		url: '/load_buttons',
		success: function(result){
			var items = GridStackUI.Utils.sort(result);
			_.each(items, function (node) {
				gridPanel.addButton(node.label, node.action, node.sequence, node.color, node.x, node.y, node.width, node.height);
			}, this);
			socket.emit('update_relays_state');
		},
		error: function(request, status, error){
			alertModal(request.responseText);
		}
	});

	return false;
}

//save the grid on the server
function saveGrid() {
	var serializedData = _.map($('.grid-stack > .grid-stack-item:visible'), function (el) {
		el = $(el);
		var node = el.data('_gridstack_node');
		var child= el.children().first();
		return {
			x: node.x,
			y: node.y,
			width: node.width,
			height: node.height,
			label: el.text(),
			action: child.data('action'),
			sequence: child.data('sequence'),
			color: child.data('color')
		};
	}, this);

	$.ajax({
		type: 'POST',
		url: '/save_buttons',
		data: {data: JSON.stringify(serializedData, null, '    ')},
		success: function(){

		},
		error: function(request, status, error){
			alertModal(request.responseText);
		}
	});

	return false;
}