var gridPanelController = {
	gridPanelView: gridPanelView,
	colorpicker: colorpicker,

	init: function() {
		this.bind();
		this.gridPanelView.init();
		this.colorpicker.init();
		//initialize the grid at his initial state in disabled edition mode
		this.loadGrid();
	},
	bind: function() {
		$("#addButton").on("click", () => {
			let buttonLabel=$("#buttonLabel").val();
			let color=$("#color").data("color");

			let action=null;
			let sequence=null;
			if ($("#relayChoice").prop("checked") == true) {
				if($("#relays").val() == null){
					failAlert("Aucun relai n'a été selectionné.");
					return;
				}
				action="relay:"+$("#relays").val();
				//if the relay isn't already used
				if(this.actionAlreadyUsed(action)){
					failAlert("Un bouton correspondant au même relai existe déjà.");
					return;
				}
			} else if ($("#sequenceChoice").prop("checked") == true) {
				if($("#sequences").val() == null){
					failAlert("Aucune séquence n'a été selectionnée.");
					return;
				}
				sequence=$("#sequences").val();
				if(this.sequenceAlreadyUsed(sequence)){
					failAlert("Un bouton correspondant à la même sequence existe déjà.");
					return;
				}
			} else if ($("#soundChoice").prop("checked") == true) {
				if($("#sounds").val() == null){
					failAlert("Aucun son n'a été selectionné.");
					return;
				}
				action="sound:"+$("#sounds").val();
				//if the sound isn't already used
				if(this.actionAlreadyUsed(action)){
					failAlert("Un bouton correspondant au même son existe déjà.");
					return;
				}
			}

			this.gridPanelView.addButton(buttonLabel, action, sequence, color, 1, 1, 1, 1);
		});

		$('input[type=radio][name=choice]').on("change", () => {
			this.gridPanelView.updateForm();
		});

		$("#editPanelButton").on("click", () => {
			this.gridPanelView.updateMode();
			this.saveGrid();
		});
	},

	/**
	 * check if a button with the same action already exists
	 */
	actionAlreadyUsed: function(label){
		let found=false;
		$('.grid-stack-item-content').each(function() {
			if($(this).data("action")===label){
				found=true;
				return false;
			}
		});
		return found;
	},

	/**
	 * check if a button with the same sequence already exists
	 */
	sequenceAlreadyUsed: function(label){
		let found=false;
		$('.grid-stack-item-content').each(function(){
			if($(this).data("sequence")===label){
				found=true;
				return false;
			}
		});
		return found;
	},

	/**
	 * load the grid from the server
	 */
	loadGrid: function(){
		this.gridPanelView.clearGrid();
		$.ajax({
			type: 'POST',
			url: '/load_buttons',
			success: (result) =>{
				let items = GridStackUI.Utils.sort(result);
				_.each(items, (node) => {
					this.gridPanelView.addButton(node.label, node.action, node.sequence, node.color, node.x, node.y, node.width, node.height);
				}, this);
				socket.emit('update_relays_state');
			},
			error: (request, status, error) =>{
				failAlert(request.responseText);
			}
		});

		return false;
	},

	/**
	 * save the grid on the server
	 */
	saveGrid: function() {
		let serializedData = _.map($('.grid-stack > .grid-stack-item:visible'), function (el) {
			el = $(el);
			let node = el.data('_gridstack_node');
			let child= el.children().first();
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
				failAlert(request.responseText);
			}
		});

		return false;
	}

};
