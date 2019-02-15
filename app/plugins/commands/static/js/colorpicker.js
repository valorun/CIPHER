var colorpicker = {
	init: function(){
		this.bind();
	},
	bind: function(){
		$("#color").on('click', function(){
			$("#color-picker").show();
		});

		//select a color and change the color of the button
		$(".color-item").on('click', function(){
			$("#color-picker").hide();
			$("#color").removeClass($("#color").data("color")); //delete the color previous color class
			let newColor=$(this).data('color');
			$("#color").data('color', newColor);
			$("#color").addClass(newColor); //add the new color
		});
	}
}