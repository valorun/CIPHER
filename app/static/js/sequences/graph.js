var nodes, edges, network;

$(document).ready(function() {
	draw();
	updateForm();

	$("#saveButton").on("click", function() {
		if(graphIsValid())
			saveGraph();
		else{
			alert("La séquence n'est pas valide, certains noeuds n'ont pas de parent.");
		}
	});

	$('input[type=radio][name=choice]').on("change", function() {
		updateForm();
	});

	$('a[name=editSeq]').on("click", function() {
		seq_name=this.id.substr(this.id.indexOf('_')+1);
		editSequence(seq_name)
	});
});

//check if all nodes have at least one parent node
function graphIsValid() {
	return nodes.get().filter(function(n) {
		return n.id != "start"
	}).every(function(n1) {
		return edges.get().some(function(e) {
			return e.to == n1.id;
		})
	});
}

//draw the graph viewer
function draw() {
        // create an array with nodes
        nodes = new vis.DataSet();
        nodes.add([{
        	id: 'start',
        	label: 'Start',
        	color: 'red'
        }]);

        // create an array with edges
        edges = new vis.DataSet();

      // create a network
      var container = document.getElementById('network');
      var data = {
      	nodes: nodes,
      	edges: edges
      };
      var locales = {
      	fr: {
      		edit: 'Editer',
      		del: 'Supprimer la sélection',
      		back: 'Retout',
      		addNode: 'Ajouter un noeud',
      		addEdge: 'Ajouter une transition',
      		editNode: 'Editer le noeud',
      		editEdge: 'Editer la transition',
      		addDescription: 'Cliquez sur un espace vide pour ajouter le noeud.',
      		edgeDescription: 'Cliquez sur un noeud et glissez la transition vers un autre pour les connecter.',
      		editEdgeDescription: 'Cliquez sur le point de controle et glissez le vers un autre noeud pour le connecter.',
      		createEdgeError: 'Cannot link edges to a cluster.',
      		deleteClusterError: 'Clusters cannot be deleted.',
      		editClusterError: 'Clusters cannot be edited.'
      	}
      };
      var options = {
      	locale: 'fr',
      	locales: locales,
      	manipulation: {
      		addNode: function(nodeData, callback) {
      			if(handleNodeToAdd(nodeData)){
      				callback(nodeData);
      			}
      			else{
      				alertModal("Le champ choisi est vide !");
      			}
      		},
      		editNode: function(nodeData, callback) {
      			if (nodeData.id !== "start") {
      				handleNodeToAdd(nodeData)
      				callback(nodeData);
      			} else{
      				alertModal("Impossible de modifier le noeud de départ.");
      				callback(null);
      			}
      		},
      		deleteNode: function(nodeData, callback) {
      			if (nodeData.nodes[0] !== "start") {
      				callback(nodeData);
      			} else{
      				alertModal("Impossible de supprimer le noeud de départ.");
      				callback(null);
      			}
      		},
      		addEdge: function(edgeData, callback) {
      			edgeData.arrows = "to";
      			callback(edgeData);
      		}
      	},
      	layout: {
      		hierarchical: {
      			enabled: true,
      			direction: 'DU',
      			sortMethod: 'directed',
      		},
          randomSeed: 2 //layout will be always the same
      }
  };
  network = new vis.Network(container, data, options);
}

//update the form to display the options corresponding to the type of button chosen
function updateForm() {
	$("#motionOptions").addClass("hide");
	$("#servoOptions").addClass("hide");
	$("#relayOptions").addClass("hide");
	$("#speechOptions").addClass("hide");
	$("#scriptOptions").addClass("hide");
	$("#soundOptions").addClass("hide");
	$("#pauseOptions").addClass("hide");
	if ($("#motionChoice").prop("checked") == true) {
		$("#motionOptions").removeClass("hide");
	} else if ($("#servoChoice").prop("checked") == true) {
		$("#servoOptions").removeClass("hide");
	} else if ($("#relayChoice").prop("checked") == true) {
		$("#relayOptions").removeClass("hide");
	} else if ($("#speechChoice").prop("checked") == true) {
		$("#speechOptions").removeClass("hide");
	} else if ($("#pauseChoice").prop("checked") == true) {
		$("#pauseOptions").removeClass("hide");
	} else if ($("#scriptChoice").prop("checked") == true) {
		$("#scriptOptions").removeClass("hide");
	} else if ($("#soundChoice").prop("checked") == true) {
		$("#soundOptions").removeClass("hide");
	}
}

//create a specific node corresponding to the option chosen
function handleNodeToAdd(nodeData) {
	var action = "";
	nodeData.shape = 'box';
	if ($("#motionChoice").prop("checked") == true) {
		action += "motion:" + $("#left").val() + "," + $("#right").val();
	} else if ($("#servoChoice").prop("checked") == true) {
		action += "servo:" + $("#sequence").val();
	} else if ($("#relayChoice").prop("checked") == true) {
		if($("#relay").val() == null)
			return false;
		action += "relay:" + $("#relay").val()+","+($("#relayOnOff").prop("checked")?1:0);
	} else if ($("#speechChoice").prop("checked") == true) {
		action += "speech:\'" + $("#sentence").val() + "\'";
	} else if ($("#scriptChoice").prop("checked") == true) {
		if($("#script").val() == null)
			return false;
		action += "script:" + $("#script").val();
	} else if ($("#soundChoice").prop("checked") == true) {
		if($("#sound").val() == null)
			return false;
		action += "sound:" + $("#sound").val();
	} else if ($("#pauseChoice").prop("checked") == true) {
		action += "pause:" + $("#pause").val() + "ms";
		nodeData.shape = "circle"
	}
	nodeData.label = action;
	return true;
}

//save the graph on the server
function saveGraph(){
  	//get the input value
  	sequence = [];
  	sequence.push(nodes.get());
  	sequence.push(edges.get());
  	console.log(sequence);
  	name=$("#name").val();

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
	json = JSON.parse($("#data_"+seq_name).text());
	nodes.clear();
	edges.clear();
	nodes.update(json[0]);
	edges.update(json[1]);
}
