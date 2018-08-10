$(document).ready(function() {
	$('input[name=enableSeq]').on("change", function() {
		var seq_name=this.id.substr(this.id.indexOf('_')+1);
		enableSequence(seq_name)
	});
	$('a[name=deleteSeq]').on("click", function() {
		var seq_name=this.id.substr(this.id.indexOf('_')+1)
		deleteSequence(seq_name)
	});

});

//enable OR disable sequence
function enableSequence(seq_name){
	$.ajax({
		type: 'POST',
		url: '/enable_sequence',
		data: {seq_name:seq_name},
		success: function(){
			console.log(seq_name+" updated");
		},
		error: function(request, status, error){
			alertModal(request.responseText);
		}
	});
}

function deleteSequence(seq_name){
	var confirm = window.confirm("Etes vous sûr de vouloir supprimer la séquence \'"+seq_name+"\' ?");
	if(confirm){
		$.ajax({
			type: 'POST',
			url: '/delete_sequence',
			data: {seq_name:seq_name},
			success: function(){
				console.log(seq_name+" deleted");
				$("#"+seq_name).remove();
			},
			error: function(request, status, error){
				alertModal(request.responseText);
			}
		});
	}
}
