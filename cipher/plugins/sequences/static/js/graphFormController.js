var graphFormController = {
	graphPanel: graphPanelController,

	init: function(){
		this.graphPanel.init();
		this.updateForm();
		this.bind();
	},
	bind: function(){
		$('#saveButton').on('click', () => {
			if(this.graphPanel.graphIsValid())
				this.saveGraph();
			else{
				failAlert('La séquence n\'est pas valide, certains noeuds n\'ont pas de parent.');
			}
		});

		$('select[name=newNodeTypeChoice]').on('change', () => {
			this.updateForm();
		});

		$('a[name=editSeq]').on('click', (e) => {
			let seq_name = e.currentTarget.id.substr(e.currentTarget.id.indexOf('_') + 1);
			this.editSequence(seq_name);
			templateController.open_accordion($('#creation'));
			window.location.hash = '#creation';
		});
	},

	/**
	* Update the form to display the options corresponding to the type of button chosen
	*/
	updateForm: function() {
		$('#motionOptions').addClass('hide');
		$('#servoOptions').addClass('hide');
		$('#relayOptions').addClass('hide');
		$('#speechOptions').addClass('hide');
		$('#scriptOptions').addClass('hide');
		$('#soundOptions').addClass('hide');
		$('#pauseOptions').addClass('hide');
		$('#conditionOptions').addClass('hide');
		$('#servoSequenceOptions').addClass('hide');//COMPATIBILITY REASON
		if($('select[name=newNodeTypeChoice]').val() !== ''){
			$('#' + $('select[name=newNodeTypeChoice]').val() + 'Options').removeClass('hide');
		}
		else{
			failAlert('Aucune action n\'a été selectionnée !');
		}
	},

	/**
	* Save the graph on the server
	*/
	saveGraph: function(){
		let sequence = [];
		sequence.push(this.graphPanel.nodes.get());
		sequence.push(this.graphPanel.edges.get());
		console.log(sequence);
		let name = $('#name').val();

		$.ajax({
			type: 'POST',
			url: '/save_sequence',
			data: {seq_name:name, seq_data : JSON.stringify(sequence, null, 4)},
			success: function(){
				location.reload();
			},
			error: function(request,){
				failAlert(request.responseText);
			}
		});
	},

	/**
	* Edit the specified sequence
	* @param {string} seq_name the name of the sequence to edit
	*/
	editSequence: function(seq_name){
		$('#name').val(seq_name);
		let json = JSON.parse($('#data_' + seq_name).text());
		this.graphPanel.nodes.clear();
		this.graphPanel.edges.clear();
		this.graphPanel.nodes.update(json[0]);
		this.graphPanel.edges.update(json[1]);
		this.graphPanel.network.focus('start');
	}
};