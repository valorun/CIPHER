var editMode=false;
var grid;


$(document).ready(function() {

	var options = {
		float: true,
		removable: '.trash',
		removeTimeout: 100,
	};

	$('#grid').gridstack(options);

	grid = $('.grid-stack').data('gridstack');

	initializeGrid();

	//button to switch mode
	$("#editPanelButton").on("click", updateMode);
});

//initialize the grid at his initial state in disabled edition mode
function initializeGrid(){
	loadGrid();
	disableEditionMode();
}


//update the display to match the selected mode
function updateMode(){
	if(editMode){
		disableEditionMode();
		grid.disable();
		saveGrid();
	}
	else{
		enableEditionMode();
		grid.enable();
	}
}

//enable edition mode, the buttons can not be clicked, but can be moved
function enableEditionMode(){
	editMode=true;
	$('.grid-stack-item-content').addClass("disabled");
	$('#editPanelButton').addClass('fa-check');
	$('#editPanelButton').removeClass('fa-edit');
	$('#newButtonPanel').removeClass('hide');
	$('.trash').removeClass('hide');
}

//disable edition mode, the buttons can not be moved, but can be clicked
function disableEditionMode(){
	editMode=false;
	$('.grid-stack-item-content').removeClass("disabled");
	$('#editPanelButton').addClass('fa-edit');
	$('#editPanelButton').removeClass('fa-check');
	$('#newButtonPanel').addClass('hide');
	$('.trash').addClass('hide');
}

//load the grid from the server
function loadGrid() {
	grid.removeAll();
	$.ajax({
		type: 'POST',
		url: '/load_buttons',
		success: function(result){
			var items = GridStackUI.Utils.sort(result);
			_.each(items, function (node) {
				addButton(node.label, node.action, node.sequence, node.color, node.x, node.y, node.width, node.height);
			}, this);
			grid.disable();
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
			color: child.css("background-color")
		};
	}, this);
	console.log(serializedData);

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

//dele all buttons on the grid
function clearGrid () {
	grid.removeAll();
	return false;
}

//add a button to the grid
//an action or a sequence can be associated if desired. if not, these values must be null
function addButton(label, action, sequence, color, x, y, width, height){
	var actionLabel="";
	if(action!=null)
		actionLabel="data-action='"+action+"' ";

	var sequenceLabel="";
	if(sequence!=null)
		sequenceLabel="data-sequence='"+sequence+"'";
	console.log(color);
	var el= $('<div><div class="grid-stack-item-content btn" style="background-color:'+color+'"'+actionLabel+sequenceLabel+'><strong class="display-middle">'+label+'</strong></div><div/>');
	if(editMode){
		el.children().first().addClass('disabled');
	}
	el.on("click", function(){
		if(!editMode){
			if(action!=null) {
				console.log(action);
				socket.emit('command', action);
			}
			if(sequence!=null) {
				console.log(sequence);
				socket.emit('play_sequence', sequence);
			}
		}
	});

	grid.addWidget(el, x, y, width, height);
	socket.emit('update_relays_state');

}

