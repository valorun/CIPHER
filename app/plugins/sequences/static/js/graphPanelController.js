var graphPanelController = {
	view: graphPanelView,

	init: function(){
		this.view.init();
		this.bind();
	},
	bind: function(){
		$("#saveButton").on("click", () => {
			if(this.view.graphIsValid())
				this.saveGraph();
			else{
				failAlert("La séquence n'est pas valide, certains noeuds n'ont pas de parent.");
			}
		});

		$('select[name=newNodeTypeChoice]').on("change", () => {
			this.view.updateForm();
		});

		$('a[name=editSeq]').on("click", (e) => {
			let seq_name=e.currentTarget.id.substr(e.currentTarget.id.indexOf('_')+1);
			this.editSequence(seq_name)
		});
	},

	/**
	* Save the graph on the server
	*/
	saveGraph: function(){
	  	let sequence = [];
	  	sequence.push(this.view.nodes.get());
	  	sequence.push(this.view.edges.get());
	  	console.log(sequence);
	  	let name=$("#name").val();

	  	$.ajax({
	  		type: 'POST',
	  		url: '/save_sequence',
	  		data: {seq_name:name, seq_data : JSON.stringify(sequence, null, 4)},
	  		success: function(){
	  			location.reload();
	  		},
	  		error: function(request, status, error){
	  			failAlert(request.responseText);
	  		}
	  	});
	},

	/**
	* Edit the specified sequence
	* @param {string} seq_name the name of the sequence to edit
	*/
	editSequence: function(seq_name){
		$("#name").val(seq_name);
		let json = JSON.parse($("#data_"+seq_name).text());
		this.view.nodes.clear();
		this.view.edges.clear();
		this.view.nodes.update(json[0]);
		this.view.edges.update(json[1]);
		this.view.network.focus("start");
	}
}
