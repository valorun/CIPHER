var raspiesController = {
	init: function(){
		this.bind();
		socket.emit('get_raspies');
	},
	bind: function(){
		$('#shutdownButton').on('click', () => {
			socket.emit('shutdown');
		});
		$('#rebootButton').on('click', () => {
			socket.emit('reboot');
		});
		socket.on('get_raspies', (raspies) => {
			console.log(raspies);
			this.updateRaspies(raspies);
		});
	},

	updateRaspies: function(raspies){
		$('#raspberries').empty();
		$.each(raspies, function(i, raspi){
			console.log(raspi);
			let card = '<div class=\'container cell center pale-green round-large border border-green padding-16\''+
							'<h3><strong><i class=\'xxxlarge fab fa-raspberry-pi\'></i></strong></h3>' +
							'<h3>' + raspi.id + '</h3>' +
						'</div>';
			$('#raspberries').append(card);
		});

	}
};
