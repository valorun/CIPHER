var relaysSettingsController = {
	init: function () {
		this.bind();
	},
	bind: function () {
		$('#addRelay').on('click', function () {
			let label = $('#newRelayLabel').val();
			let pin = $('#newRelayPin').val();
			let parity = $('#newRelayParity').val();
			let raspi_id = $('#newRelayRaspiId').val();

			$.ajax({
				type: 'POST',
				url: '/save_relay',
				data: { rel_label: label, rel_pin: pin, rel_parity: parity, raspi_id: raspi_id },
				success: function () {
					location.reload();
				},
				error: function (request) {
					failAlert(request.responseText);
				}
			});
			//location.reload();
		});
		//checkbox to enable or disable the relay
		$('input[name=enableRel]').on('change', (e) => {
			let rel_label = e.currentTarget.id.substr(e.currentTarget.id.indexOf('_') + 1);
			this.enableRelay(rel_label, $(e.currentTarget).prop('checked'));
		});

		//button to delete the relay
		$('a[name=deleteRel]').on('click', (e) => {
			let rel_label = e.currentTarget.id.substr(e.currentTarget.id.indexOf('_') + 1);
			this.deleteRelay(rel_label);
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
				console.log(rel_label + ' updated');
			},
			error: function (request) {
				failAlert(request.responseText);
			}
		});
	},

	/**
 	 *  Delete a relay
 	 *	@param	{string} rel_label relay label
 	 */
	deleteRelay: function (rel_label) {
		var confirm = window.confirm('Etes vous sûr de vouloir supprimer le relai \'' + rel_label + '\' ?');
		if (confirm) {
			$.ajax({
				type: 'POST',
				url: '/delete_relay',
				data: { rel_label: rel_label },
				success: () => {
					console.log(rel_label + ' deleted');
					$('#' + rel_label).remove();
				},
				error: (request) => {
					failAlert(request.responseText);
				}
			});
		}
	}
};
