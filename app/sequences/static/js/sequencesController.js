var sequencesController = {
	init: function(){
		this.bind();
	},
	bind: function(){
		$('input[name=enableSeq]').on("change", (e) => {
			//get the sequence name by getting the second part of the id, after '_'
			let seq_name=e.currentTarget.id.substr(e.currentTarget.id.indexOf('_')+1);
			this.enableSequence(seq_name, $(e.currentTarget).prop("checked"))
		});
		$('a[name=deleteSeq]').on("click", (e) => {
			//get the sequence name by getting the second part of the id, after '_'
			let seq_name=e.currentTarget.id.substr(e.currentTarget.id.indexOf('_')+1)
			this.deleteSequence(seq_name)
		});
	},

	/**
	* enable OR disable a sequence
	* @param {string} seq_name the name of the sequence to enable or disable
	* @param {boolean} value the new state for the sequence
	*/
	enableSequence: function(seq_name, value){
		$.ajax({
			type: 'POST',
			url: '/enable_sequence',
			data: {seq_name:seq_name, value:value},
			success: function(){
				console.log(seq_name+" updated");
			},
			error: function(request, status, error){
				failAlert(request.responseText);
			}
		});
	},

	/**
	* completely delete a sequence
	* @param {string} seq_name the name of the sequence to delete
	*/
	deleteSequence: function(seq_name){
		let confirm = window.confirm("Etes vous sûr de vouloir supprimer la séquence \'"+seq_name+"\' ?");
		if(confirm){
			$.ajax({
				type: 'POST',
				url: '/delete_sequence',
				data: {seq_name:seq_name},
				success: function(){
					console.log(seq_name+" deleted");
					$("#"+seq_name).remove();
				},
				error: function(request, status, error){
					failAlert(request.responseText);
				}
			});
		}
	}
}
