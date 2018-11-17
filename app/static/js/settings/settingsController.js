var settingsController = {
	init: function () {
		window.speechSynthesis.onvoiceschanged = function () {
			let voices = window.speechSynthesis.getVoices();
			$.each(voices, function () {
				if (typeof Cookies.get('voice') !== 'undefined' &&
					Cookies.get('voice') === this.name) { // if a voice has already been chosen, select it
					$("#voices").append($("<option selected='selected'/>").val(this.name).text(this.name));
				} else {
					$("#voices").append($("<option />").val(this.name).text(this.name));
				}
			});
		};
		this.bind();
		socket.emit("get_raspies");
	},
	bind: function () {
		$("#addRelay").on("click", function () {
			let label = $("#newLabel").val();
			let pin = $("#newPin").val();
			let parity = $("#newParity").val();
			let raspi_id = $("#newRaspiId").val();

			$.ajax({
				type: 'POST',
				url: '/save_relay',
				data: { rel_label: label, rel_pin: pin, rel_parity: parity, raspi_id: raspi_id },
				success: function () {
					location.reload();
				},
				error: function (request, status, error) {
					failAlert(request.responseText);
				}
			});
			//location.reload();
		});
		//checkbox to enable or disable the relay
		$('input[name=enableRel]').on("change", (e) => {
			let rel_label = e.currentTarget.id.substr(e.currentTarget.id.indexOf('_') + 1)
			this.enableRelay(rel_label, $(e.currentTarget).prop("checked"))
		});

		//button to delete the relay
		$('a[name=deleteRel]').on("click", (e) => {
			let rel_label = e.currentTarget.id.substr(e.currentTarget.id.indexOf('_') + 1)
			this.deleteRelay(rel_label)
		});

		//voice selection
		$("#voices").on("change", function () {
			Cookies.set("voice", $("#voices").val());
		})

		socket.on('get_raspies', (raspies) => {
			raspies = raspies.map(r => r.id);
			$("#newRaspiId").autocomplete({
				source: raspies
			});
		});

		//camera url modification
		$("#cameraUrlForm").on("submit", (e) => {
			e.preventDefault();
			$.ajax({
				type: 'POST',
				url: '/update_camera_url',
				data: { camera_url: $("#cameraUrl").val() },
				success: function () {
					successAlert("L'URL de la caméra a été mis à jour");
				},
				error: function (request, status, error) {
					failAlert(request.responseText);
				}
			});
		});

		//motion mode
		$("#wheelsMode").on("change", (e) => {
			$.ajax({
				type: 'POST',
				url: '/update_motion_mode',
				data: { value: $(e.currentTarget).prop("checked") },
				success: function () {
					successAlert("Le mode de déplacement a été mis à jour");
				},
				error: function (request, status, error) {
					failAlert(request.responseText);
				}
			});
		});

		//audio on server mode
		$("#audioOnServer").on("change", (e) => {
			$.ajax({
				type: 'POST',
				url: '/update_audio_source',
				data: { value: $(e.currentTarget).prop("checked") },
				success: function () {
					successAlert("La source audio a été mise à jour");
				},
				error: function (request, status, error) {
					failAlert(request.responseText);
				}
			});
		});

		//chatbot readd only mode
		$("#chatbotReadOnlyMode").on("change", (e) => {
			$.ajax({
				type: 'POST',
				url: '/update_chatbot_learning_mode',
				data: { value: $(e.currentTarget).prop("checked") },
				success: function () {
					successAlert("Le mode d'apprentissage du chatbot a été mis à jour");
				},
				error: function (request, status, error) {
					failAlert(request.responseText);
				}
			});
		});

	},

	/**
 	 *  Enable OR disable a relay
	  *	@param	{string} rel_label relay label
	  *	@param	{boolean} value new state for the relay
 	 */
	enableRelay: function (rel_label, value) {
		$.ajax({
			type: 'POST',
			url: '/enable_relay',
			data: { rel_label: rel_label, value: value },
			success: function () {
				console.log(rel_label + " updated");
			},
			error: function (request, status, error) {
				failAlert(request.responseText);
			}
		});
	},

	/**
 	 *  Delete a relay
 	 *	@param	{string} rel_label relay label
 	 */
	deleteRelay: function (rel_label) {
		var confirm = window.confirm("Etes vous sûr de vouloir supprimer le relai \'" + rel_label + "\' ?");
		if (confirm) {
			$.ajax({
				type: 'POST',
				url: '/delete_relay',
				data: { rel_label: rel_label },
				success: () => {
					console.log(rel_label + " deleted");
					$("#" + rel_label).remove();
				},
				error: (request, status, error) => {
					failAlert(request.responseText);
				}
			});
		}
	}
}
