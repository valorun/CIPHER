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

			let actionType = $('select[name=newButtonTypeChoice]').val();
			let actionParam=null;
			let actionFlags=null;
			if (actionType == "relay") {
				if($("#relays").val() == null){
					failAlert("Aucun relai n'a été selectionné.");
					return;
				}
				actionParam=$("#relays").val();
				//if the relay isn't already used
				if(this.actionAlreadyUsed(actionParam, "relay")){
					failAlert("Un bouton correspondant au même relai existe déjà.");
					return;
				}
			} else if (actionType == "sequence") {
				if($("#sequences").val() == null){
					failAlert("Aucune séquence n'a été selectionnée.");
					return;
				}
				actionParam=$("#sequences").val();
				if(this.actionAlreadyUsed(actionParam, "sequence")){
					failAlert("Un bouton correspondant à la même sequence existe déjà.");
					return;
				}
				actionFlags=$("#flags").val().split(' ');
			} else if (actionType == "sound") {
				if($("#sounds").val() == null){
					failAlert("Aucun son n'a été selectionné.");
					return;
				}
				actionParam=$("#sounds").val();
				//if the sound isn't already used
				if(this.actionAlreadyUsed(actionParam)){
					failAlert("Un bouton correspondant au même son existe déjà.");
					return;
				}
			}

			this.gridPanelView.addButton(buttonLabel, actionType, actionParam, actionFlags, color, 1, 1, 1, 1);
		});

		$('select[name=newButtonTypeChoice]').on("change", () => {
			this.gridPanelView.updateForm();
		});

		$("#editPanelButton").on("click", () => {
			this.gridPanelView.updateMode();
			this.saveGrid();
			socket.emit('update_all_relays_state');
		});
	},

	/**
	 * Check if a button with the same action already exists
	 */
	actionAlreadyUsed: function(label, type){
		let found=false;
		$('.grid-stack-item-content').each(function() {
			if($(this).data(type)===label){
				found=true;
				return false;
			}
		});
		return found;
	},

	/**
	 * Load the grid from the server
	 */
	loadGrid: function(){
		this.gridPanelView.clearGrid();
		$.ajax({
			type: 'POST',
			url: '/load_buttons',
			success: (result) =>{
				let items = GridStackUI.Utils.sort(result);
				_.each(items, (node) => {
					flags = [];
					if(node.action.flags != null)
						flags = node.action.flags.split(' ');
					this.gridPanelView.addButton(node.label, node.action.type, node.action.parameter, flags, node.color, node.x, node.y, node.width, node.height);
				}, this);
				socket.emit('update_all_relays_state');
			},
			error: (request, status, error) =>{
				failAlert(request.responseText);
			}
		});

		return false;
	},

	/**
	 * Save the grid on the server
	 */
	saveGrid: function() {
		let serializedData = _.map($('.grid-stack > .grid-stack-item:visible'), function (el) {
			el = $(el);
			let node = el.data('_gridstack_node');
			let child= el.children().first();
			let action = {};
			action.type = child.data('type');
			action.parameter = child.data('parameter');
			action.flags = child.data('flags')

			return {
				x: node.x,
				y: node.y,
				width: node.width,
				height: node.height,
				label: el.text(),
				action: action,
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
