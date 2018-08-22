let graphPanel = null;

$(document).ready(function() {
	graphPanel = new GraphPanel();

	$("#saveButton").on("click", function() {
		if(graphPanel.graphIsValid())
			saveGraph();
		else{
			alertModal("La séquence n'est pas valide, certains noeuds n'ont pas de parent.");
		}
	});

	$('input[type=radio][name=choice]').on("change", function() {
		graphPanel.updateForm();
	});

	$('a[name=editSeq]').on("click", function() {
		seq_name=this.id.substr(this.id.indexOf('_')+1);
		editSequence(seq_name)
	});
});

//save the graph on the server
function saveGraph(){
  	//get the input value
  	let sequence = [];
  	sequence.push(graphPanel.nodes.get());
  	sequence.push(graphPanel.edges.get());
  	console.log(sequence);
  	let name=$("#name").val();

  	$.ajax({
  		type: 'POST',
  		url: '/save_sequence',
  		data: {seq_name:name, seq_data : JSON.stringify(sequence, null, 4)},
  		success: function(){
  			location.reload();
  		},
  		error: function(request, status, error){
  			alertModal(request.responseText);
  		}
  	});
}

//edit the specified sequence
function editSequence(seq_name){
	$("#name").val(seq_name);
	let json = JSON.parse($("#data_"+seq_name).text());
	graphPanel.nodes.clear();
	graphPanel.edges.clear();
	graphPanel.nodes.update(json[0]);
	graphPanel.edges.update(json[1]);
}