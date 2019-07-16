var raspiesController = {
	init: function(){
		this.bind();
		socket.emit('get_raspies');
	},
	bind: function(){
		document.getElementById('shutdownButton').addEventListener('click', () => {
			socket.emit('shutdown');
		});
		document.getElementById('rebootButton').addEventListener('click', () => {
			socket.emit('reboot');
		});
		socket.on('get_raspies', (raspies) => {
			this.updateRaspies(raspies);
		});
	},

	updateRaspies: function(raspies){
		document.getElementById('raspberries').innerHTML = '';

		raspies.array.forEach(raspi => {
			console.log(raspi);
			let card = '<div class=\'container cell center pale-green round-large border border-green padding-16\''+
							'<h3><strong><i class=\'xxxlarge fab fa-raspberry-pi\'></i></strong></h3>' +
							'<h3>' + raspi.id + '</h3>' +
						'</div>';
			document.getElementById('raspberries').insertAdjacentElement('beforeend', card);
		});

	}
};
