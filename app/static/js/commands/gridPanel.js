function GridPanel(gridElement, editPanelButton, addButtonPanel){
	editMode=false;
	let self=this;

	let callbacks = {};
	triggerEvent = function(event){
       for (var i=0; event in callbacks && i<callbacks[event].length; i++)
            callbacks[event][i]();
	};
	self.addListener = function(event, handler){
		if (event in callbacks)
            callbacks[event].push(handler);
        else
            callbacks[event] = [handler];
	};

	let options = {
		float: true,
		removable: '.trash',
		removeTimeout: 100,
	};

	gridElement.gridstack(options);
	var grid = $('.grid-stack').data('gridstack');

	//update status information about a specified relay
	socket.on('update_relay_state', function(relay) {
		$( "div[data-action='relay:"+relay.label+"']" ).each(function(){
			console.log(relay);
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

	//enable edition mode, the buttons can not be clicked, but can be moved
	enableEditionMode = function(){
		editMode=true;
		$('.grid-stack-item-content').addClass("disabled");
		editPanelButton.addClass('fa-check');
		editPanelButton.removeClass('fa-edit');
		addButtonPanel.removeClass('hide');
		$('.trash').removeClass('hide');
	}

	//disable edition mode, the buttons can not be moved, but can be clicked
	disableEditionMode = function(){
		editMode=false;
		$('.grid-stack-item-content').removeClass("disabled");
		editPanelButton.addClass('fa-edit');
		editPanelButton.removeClass('fa-check');
		addButtonPanel.addClass('hide');
		$('.trash').addClass('hide');
	}

	//load the grid from the server
	self.loadGrid = function() {
		grid.removeAll();
		$.ajax({
			type: 'POST',
			url: '/load_buttons',
			success: function(result){
				var items = GridStackUI.Utils.sort(result);
				_.each(items, function (node) {
					self.addButton(node.label, node.action, node.sequence, node.color, node.x, node.y, node.width, node.height);
				}, this);
				grid.disable();
				socket.emit('update_relays_state');
			},
			error: function(request, status, error){
				triggerEvent();
				alertModal(request.responseText);
			}
		});

		return false;
	}

	//save the grid on the server
	self.saveGrid = function() {
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

	//delete all buttons on the grid
	self.clearGrid = function() {
		grid.removeAll();
		return false;
	}

	//add a button to the grid
	//an action or a sequence can be associated if desired. if not, these values must be null
	self.addButton = function(label, action, sequence, color, x, y, width, height){
		var actionLabel="";
		if(action!=null)
			actionLabel="data-action='"+action+"' ";

		var sequenceLabel="";
		if(sequence!=null)
			sequenceLabel="data-sequence='"+sequence+"'";

		var colorData="";
		if(color!=null)
			colorData="data-color='"+color+"'";

		console.log(color);
		var el= $('<div><div class="grid-stack-item-content btn '+ color +'" '+ colorData + actionLabel+sequenceLabel+'><strong class="display-middle">'+label+'</strong></div><div/>');
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
	};

	//update the display to match the selected mode
	updateMode = function(){
		if(editMode){
			disableEditionMode();
			grid.disable();
			self.saveGrid();
		}
		else{
			enableEditionMode();
			grid.enable();
		}
	};

	//initialize the grid at his initial state in disabled edition mode
	self.loadGrid();
	disableEditionMode();
	editPanelButton.on("click", updateMode);
}