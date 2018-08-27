var settingsController = {
	init: function(){
		window.speechSynthesis.onvoiceschanged = function() {
    		let voices=window.speechSynthesis.getVoices();
    		$.each(voices,function(){
    			if(typeof Cookies.get('voice') !== 'undefined' &&
              	Cookies.get('voice') === this.name){ // if a voice has already been chosen, select it
    				$("#voices").append($("<option selected='selected'/>").val(this.name).text(this.name));
    			}else {
    				$("#voices").append($("<option />").val(this.name).text(this.name));
    			}
    		});
    	};
		this.bind();
		socket.emit("get_raspies");
	},
	bind: function(){
		$("#addRelay").on("click", function(){
			let label=$("#newLabel").val();
			let pin=$("#newPin").val();
			let parity=$("#newParity").val();
			let raspi_id=$("#newRaspiId").val();

			$.ajax({
				type: 'POST',
				url: '/save_relay',
				data: {rel_label:label, rel_pin:pin, rel_parity:parity, raspi_id:raspi_id},
				success: function(){
					location.reload();
				},
				error: function(request, status, error){
					failAlert(request.responseText);
				}
			});
   			//location.reload();
		});
		//checkbox to enable or disable the relay
    	$('input[name=enableRel]').on("change", (e) => {
    		let rel_label=e.currentTarget.id.substr(e.currentTarget.id.indexOf('_')+1)
    		this.enableRelay(rel_label)
    	});

    	//button to delete the relay
   		$('a[name=deleteRel]').on("click", (e) => {
    		let rel_label=e.currentTarget.id.substr(e.currentTarget.id.indexOf('_')+1)
    		this.deleteRelay(rel_label)
    	});

    	$("#voices").on("change", function() {
    		Cookies.set("voice", $("#voices").val());
    	})

		socket.on('get_raspies', (raspies) => {
			raspies = raspies.map(r => r.id);
			$("#newRaspiId").autocomplete({
				source: raspies
			});
		});

	},

	/**
 	 *  Enable OR disable a relay
 	 *	@param	{string} rel_label relay label
 	 */
 	enableRelay: function(rel_label){
 		$.ajax({
 			type: 'POST',
 			url: '/enable_relay',
 			data: {rel_label:rel_label},
 			success: function(){
 				console.log(rel_label+" updated");
 			},
 			error: function(request, status, error){
 				failAlert(request.responseText);
 			}
 		});
 	},

	/**
 	 *  Delete a relay
 	 *	@param	{string} rel_label relay label
 	 */
 	deleteRelay: function(rel_label){
 		var confirm = window.confirm("Etes vous sûr de vouloir supprimer le relai \'"+rel_label+"\' ?");
 		if(confirm){
 			$.ajax({
 				type: 'POST',
 				url: '/delete_relay',
 				data: {rel_label:rel_label},
 				success: function(){
 					console.log(rel_label+" deleted");
 					$("#"+rel_label).remove();
 				},
 				error: function(request, status, error){
 					failAlert(request.responseText);
 				}
 			});
 		}
 	}
}
