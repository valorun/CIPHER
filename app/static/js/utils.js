function alertModal(message){
	$('.alert-modal')
	.append("<div class='display-bottomright'>"+
				"<div class='panel card-4 dark-red animate-bottom display-container'>"+
					"<span onclick=this.parentElement.style.display='none'' "+
						"class='button dark-red large display-topright'>&times;"+
					"</span>"+
					"<p class='container'>"+
						"<h3>"+message+"</h3>"+
					"</p>"+
				"</div>"+
			"</div>");
	setTimeout(function(){
			$('.alert-modal').empty();
	}, 3000);
}