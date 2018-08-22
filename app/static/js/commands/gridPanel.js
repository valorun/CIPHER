function GridPanel(gridElement, editPanelButton, addButtonPanel){
	let editMode = false;
	let self = this;

	let callbacks = {};
	let triggerEvent = function(event){
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
	let enableEditionMode = function(){
		editMode=true;
		$('.grid-stack-item-content').addClass("disabled");
		editPanelButton.addClass('fa-check');
		editPanelButton.removeClass('fa-edit');
		addButtonPanel.removeClass('hide');
		$('.trash').removeClass('hide');
	}

	//disable edition mode, the buttons can not be moved, but can be clicked
	let disableEditionMode = function(){
		editMode=false;
		$('.grid-stack-item-content').removeClass("disabled");
		editPanelButton.addClass('fa-edit');
		editPanelButton.removeClass('fa-check');
		addButtonPanel.addClass('hide');
		$('.trash').addClass('hide');
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

		var el= $('<div><div class="grid-stack-item-content btn '+ color +'" '+ colorData + actionLabel+sequenceLabel+'><strong class="display-middle">'+label+'</strong></div><div/>');
		if(editMode){
			el.children().first().addClass('disabled');
		}
		el.on("click", function(){
			if(!editMode){
				if(action!=null) {
					//console.log(action);
					socket.emit('command', action);
				}
				if(sequence!=null) {
					//console.log(sequence);
					socket.emit('play_sequence', sequence);
				}
			}
		});
		grid.addWidget(el, x, y, width, height);
		socket.emit('update_relays_state');
	};

	//update the display to match the selected mode
	self.updateMode = function(){
		if(editMode){
			disableEditionMode();
			grid.disable();
		}
		else{
			enableEditionMode();
			grid.enable();
		}
	};

	self.updateForm = function() {
		$("#relays").addClass("hide");
		$("#sequences").addClass("hide");
		$("#sounds").addClass("hide");
		if ($("#relayChoice").prop("checked") == true) {
			$("#relays").removeClass("hide");
		} else if ($("#sequenceChoice").prop("checked") == true) {
			$("#sequences").removeClass("hide");
		} else if ($("#soundChoice").prop("checked") == true) {
			$("#sounds").removeClass("hide");
		}
	}
	disableEditionMode();
}