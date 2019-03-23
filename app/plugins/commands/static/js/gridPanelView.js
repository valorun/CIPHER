var gridPanelView = {

	editionMode: false,

	gridOptions: {
		float: true,
		removable: '.trash',
		removeTimeout: 100,
	},

	grid: null,

	init: function(){
		$('#grid').gridstack(this.gridOptions);
		this.grid = $('.grid-stack').data('gridstack');
		this.disableEditionMode();
		this.bind();
	},

	bind: function(){
		//update status information about a specified relay
		socket.on('update_relays_state', function(relays_list) {
			console.log(relays_list);
			console.log(relays_list.relays);
			$( relays_list.relays ).each((i, relay) => {
				//get the relays and their parameter (the relay specified), and update the associated state
				$( "div[data-type='relay' data-parameter='"+relay.label+"']" ).each((i, e) => {
					$(e).addClass('border');
					$(e).css({"border-width":"3px"})
					if(relay.state===1){
						$(e).addClass('border-green');
						$(e).removeClass('border-dark-red');
					}
					else if(relay.state===0){
						$(e).addClass('border-dark-red');
						$(e).removeClass('border-green');
					}
				})
			})
		});
	},

	/**
	 * Enable edition mode, the buttons can not be clicked, but can be moved
	 */
	enableEditionMode: function(){
		this.editionMode=true;
		$('.grid-stack-item-content').addClass("disabled");
		$("#editPanelButton").addClass('fa-check');
		$("#editPanelButton").removeClass('fa-edit');
		$('#newButtonPanel').removeClass('hide');
		$('.trash').removeClass('hide');
	},

	/**
	 * Disable edition mode, the buttons can not be moved, but can be clicked
	 */
	disableEditionMode: function(){
		this.editionMode=false;
		$('.grid-stack-item-content').removeClass("disabled");
		$("#editPanelButton").addClass('fa-edit');
		$("#editPanelButton").removeClass('fa-check');
		$('#newButtonPanel').addClass('hide');
		$('.trash').addClass('hide');
	},


	/**
	 * Delete all buttons on the grid
	 */
	clearGrid: function() {
		this.grid.removeAll();
		return false;
	},

	/**
	 * Add a button to the grid
	 * An action can be associated if desired. Additional parameters can be specified
	 */
	addButton: function(label, actionType, actionParameter, actionFlags, color, x, y, width, height){
		let dataType = 'data-type="' + actionType + '" ';
		let dataParameter = 'data-parameter="' + actionParameter + '" ';
		let dataFlags = "";
		if(actionFlags != null)
			dataFlags = 'data-flags="' + actionFlags.join(' ') + '" ';
		
		var dataColor="";
		if(color!=null)
		dataColor='data-color="'+color+'"';

		var el= $('<div><div class="grid-stack-item-content btn '+ color +'" ' + dataType + dataParameter + dataFlags + dataColor+ '><strong class="display-middle">' + label + '</strong></div><div/>');
		if(this.editionMode){
			el.children().first().addClass('disabled');
		}
		el.on("click", () =>{
			if(!this.editionMode){
				if(actionType == "relay") {
					socket.emit('activate_relay', actionParameter);
				}
				if(actionType == "sequence") {
					socket.emit('play_sequence', actionParameter, actionFlags);
				}
				if(actionType == "sound") {
					socket.emit('play_sound', actionParameter);
				}
				console.log(actionType + ", " + actionParameter + ", " + actionFlags);
			}
		});
		this.grid.addWidget(el, x, y, width, height);
		socket.emit('update_all_relays_state');
	},

	/**
	 * Update the display to match the selected mode
	 */
	updateMode: function(){
		if(this.editionMode){
			this.disableEditionMode();
			this.grid.disable();
		}
		else{
			this.enableEditionMode();
			this.grid.enable();
		}
	},

	/**
	 * Update the form to match selected options
	 */
	updateForm: function() {
		$("#relayOptions").addClass("hide");
		$("#sequenceOptions").addClass("hide");
		$("#soundOptions").addClass("hide");
		if($('select[name=newButtonTypeChoice]').val()!==""){
			$("#" +$('select[name=newButtonTypeChoice]').val()+ "Options").removeClass("hide");
		}
		else{
			failAlert("Aucun type de bouton n'a été selectionné !");
		}
	}
}
