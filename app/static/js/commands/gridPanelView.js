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
		socket.on('update_relay_state', function(relay) {
			$( "div[data-action='relay:"+relay.label+"']" ).each((i, e) => {
				$(e).addClass('border');
				$(e).css({"border-width":"2px"})
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
	},

	/**
	 * enable edition mode, the buttons can not be clicked, but can be moved
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
	 * disable edition mode, the buttons can not be moved, but can be clicked
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
	 * delete all buttons on the grid
	 */
	clearGrid: function() {
		this.grid.removeAll();
		return false;
	},

	/**
	 * add a button to the grid
	 * an action or a sequence can be associated if desired. if not, these values must be null
	 */
	addButton: function(label, action, sequence, color, x, y, width, height){
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
		if(this.editionMode){
			el.children().first().addClass('disabled');
		}
		el.on("click", () =>{
			if(!this.editionMode){
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
		this.grid.addWidget(el, x, y, width, height);
		socket.emit('update_relays_state');
	},

	/**
	 * update the display to match the selected mode
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
	 * update the form to match selected options
	 */
	updateForm: function() {
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
}
