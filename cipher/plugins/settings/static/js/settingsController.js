var settingsController = {
	init: function () {
		window.speechSynthesis.onvoiceschanged = this.fillVoices;
		this.bind();
		this.fillVoices();
		socket.emit('get_raspies');
	},
	bind: function () {

		//voice selection
		$('#voices').on('change', function () {
			Cookies.set('voice', $('#voices').val());
		})

		socket.on('get_raspies', (raspies) => {
			raspies = raspies.map(r => r.id);
			$('#newRelayRaspiId,#newServoRaspiId,#motionRaspiId,#servoRaspiId').autocomplete({
				source: raspies
			});

		});
		

		//camera url modification
		$('#cameraUrlForm').on('submit', (e) => {
			e.preventDefault();
			$.ajax({
				type: 'POST',
				url: '/update_camera_url',
				data: { camera_url: $('#cameraUrl').val() },
				success: function () {
					successAlert('L\'URL de la caméra a été mis à jour');
				},
				error: function (request) {
					failAlert(request.responseText);
				}
			});
		});

		//motion mode
		$('#wheelsMode').on('change', (e) => {
			$.ajax({
				type: 'POST',
				url: '/update_motion_mode',
				data: { value: $(e.currentTarget).prop('checked') },
				success: function () {
					successAlert('Le mode de déplacement a été mis à jour');
				},
				error: function (request) {
					failAlert(request.responseText);
				}
			});
		});

		//audio on server mode
		$('#audioOnServer').on('change', (e) => {
			$.ajax({
				type: 'POST',
				url: '/update_audio_source',
				data: { value: $(e.currentTarget).prop('checked') },
				success: function () {
					successAlert('La source audio a été mise à jour');
				},
				error: function (request) {
					failAlert(request.responseText);
				}
			});
		});

		//motion raspi id modification
		$('#motionRaspiIdForm').on('submit', (e) => {
			e.preventDefault();
			$.ajax({
				type: 'POST',
				url: '/update_motion_raspi_id',
				data: { raspi_id: $('#motionRaspiId').val() },
				success: function () {
					successAlert('L\'id du raspberry chargé des déplacements a été mis à jour');
				},
				error: function (request) {
					failAlert(request.responseText);
				}
			});
		});

		//robot name modification
		$('#robotNameForm').on('submit', (e) => {
			e.preventDefault();
			$.ajax({
				type: 'POST',
				url: '/update_robot_name',
				data: { robot_name: $('#robotName').val() },
				success: function () {
					successAlert('Le nom du robot a été mis à jour');
				},
				error: function (request) {
					failAlert(request.responseText);
				}
			});
		});

	},
	fillVoices: function() {
		let voices = window.speechSynthesis.getVoices();
		$('#voices').empty();
		$.each(voices, function () {
			if (typeof Cookies.get('voice') !== 'undefined' &&
				Cookies.get('voice') === this.name) { // if a voice has already been chosen, select it
				$('#voices').append($('<option selected=\'selected\'/>').val(this.name).text(this.name));
			} else {
				$('#voices').append($('<option />').val(this.name).text(this.name));
			}
		});
	}
};
