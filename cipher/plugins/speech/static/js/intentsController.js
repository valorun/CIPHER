var intentsController = {
	init: function(){
		this.bind();
	},
	bind: function(){
		//button to add the sentence to the conversation
  		$("#addResponseButton").on("click", () => {
  			var intent=$( "#currentIntent" ).val();
  			if(intent==null || intent===""){
				failAlert("L'intention fournie est vide.");
  				return;
			}
			var response=$("#currentResponse" ).val()
  			var sequence_id=$( "#currentSequence" ).val();
			$.ajax({
				type: 'POST',
				url: '/save_intent',
				data: { intent: intent, response: response, sequence_id: sequence_id},
				success: function () {
					location.reload();
				},
				error: function (request, status, error) {
					failAlert(request.responseText);
				}
			});
		});
		//checkbox to enable or disable the relay
		$('input[name=enableIntent]').on("change", (e) => {
			let intent = e.currentTarget.id.substr(e.currentTarget.id.indexOf('_') + 1)
			this.enableIntent(intent, $(e.currentTarget).prop("checked"))
		});

		//button to delete the relay
		$('a[name=deleteIntent]').on("click", (e) => {
			let intent = e.currentTarget.id.substr(e.currentTarget.id.indexOf('_') + 1)
			this.deleteIntent(intent)
		});
	},

	/**
 	 *  Enable OR disable an intent
	  *	@param	{string} intent intant name
	  *	@param	{boolean} value new state for the intent
 	 */
	 enableIntent: function (intent, value) {
		$.ajax({
			type: 'POST',
			url: '/enable_intent',
			data: { intent: intent, value: value },
			success: function () {
				console.log(intent + " updated");
			},
			error: function (request, status, error) {
				failAlert(request.responseText);
			}
		});
	},

	/**
 	 *  Delete an intent
 	 *	@param	{string} intent intent name
 	 */
	deleteIntent: function (intent) {
		var confirm = window.confirm("Etes vous sûr de vouloir supprimer l'intention \'" + intent + "\' ?");
		if (confirm) {
			$.ajax({
				type: 'POST',
				url: '/delete_intent',
				data: { intent: intent },
				success: () => {
					console.log(intent + " deleted");
					$("#" + intent).remove();
				},
				error: (request, status, error) => {
					failAlert(request.responseText);
				}
			});
		}
	}
}
