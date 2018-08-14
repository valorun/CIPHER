function alertModal(message){
	$('.alert-modal')
	.append("<div class='display-bottomright'>"+
				"<div class='panel card-4 dark-red animate-bottom display-container'>"+
					"<span onclick=\"this.parentElement.style.display='none'\" "+
						"class='button dark-red large display-topright'>&times;"+
					"</span>"+
					"<h3>Attention !</h3>" +
					"<p>"+
						"<strong>"+message+"</strong>"+
					"</p>"+
				"</div>"+
			"</div>");
	setTimeout(function(){
			$('.alert-modal').empty();
	}, 3000);
}