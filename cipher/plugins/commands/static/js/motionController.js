var motionController = {
	key_pressed: false,
	init: function () {
		this.bind();
	},
	bind: function () {
		$('#motion_speed').slider({
			orientation: 'vertical',
			range: 'min',
			min: 0,
			max: 100,
			value: 0,
			slide: (event, ui) => {
				$('#amount').val(ui.value);
			}
		});

		//selects different listeners depending on the type of device used.
		let startActionEvent = 'mousedown';
		let stopActionEvent = 'mouseup'; //mouseleave if we also want to stop when the cursor is out of the button
		if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
			startActionEvent = 'touchstart';
			stopActionEvent = 'touchend';
		}

		//carriage panel controller
		$('.motion-direction').on(startActionEvent, (e) => {
			let direction = $(e.currentTarget).attr('value').split('_')[1];
			let speed = $('#motion_speed').slider('value');

			console.log(direction + ', ' + speed);
			socket.emit('move', direction, speed);
		}).on(stopActionEvent, () => {
			console.log('stop, 0');
			socket.emit('move', 'stop', 0);
		});

		//carriage key controller
		$(document).on('keydown', (e) => {
			if (!templateController.is_accordion_open($('#motion')))
				return;
			e.preventDefault();
			if (this.key_pressed)
				return;
			let direction = 'stop';
			let speed = $('#motion_speed').slider('value');

			switch (e.keyCode) {
				case 37:
					direction = 'left';
					break;
				case 38:
					direction = 'forwards';
					break;
				case 39:
					direction = 'right';
					break;
				case 40:
					direction = 'backwards';
					break;
			}
			console.log(direction + ', ' + speed);
			socket.emit('move', direction, speed);
			this.key_pressed = true;
		}).on('keyup', () => {
			if (!templateController.is_accordion_open($('#motion')))
				return;
			console.log('stop, 0');
			socket.emit('move', 'stop', 0);
			this.key_pressed = false;
		});
	}
};