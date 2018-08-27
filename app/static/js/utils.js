function failAlert(message){
	alert("<i class='fas fa-times-circle'></i> Attention !", message, "dark-red");
}
function successAlert(message){
	alert("<i class='fas fa-check-circle'></i> Succès !", message, "green");
}

function alert(title, message, color){
	$('.alert-modal')
	.append("<div class='display-bottomright'>"+
				"<div class='panel card-4 animate-bottom display-container "+color+"'>"+
					"<span onclick=\"this.parentElement.style.display='none'\" "+
						"class='button large display-topright "+color+"'>&times;"+
					"</span>"+
					"<h3>"+title+"</h3>" +
					"<p>"+
						"<strong>"+message+"</strong>"+
					"</p>"+
				"</div>"+
			"</div>");
	setTimeout(function(){
			$('.alert-modal').empty();
	}, 3000);
}

function linebreak(s) {
	const two_line = /\n\n/g;
	const one_line = /\n/g;
	return s.replace(two_line, '<p/>').replace(one_line, '<br>');
}

function capitalize(s) {
	return s.replace(s.substr(0,1), function(m) { return m.toUpperCase(); });
}
