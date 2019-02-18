var graphPanelView = {
	nodes: null,
	edges: null,
	network: null,

	init: function(){
		this.updateForm();
		this.bind();
		this.render();
	},
	bind: function(){

	},
	render: function(){
		// create an array with nodes
		this.nodes = new vis.DataSet();
		this.nodes.add([{
			id: 'start',
			label: 'Start',
			color: 'red'
		}]);

		// create an array with edges
		this.edges = new vis.DataSet();
		
		// create a network
		let container = document.getElementById('network');
		let data = {
			nodes: this.nodes,
			edges: this.edges
		};
		let locales = {
			fr: {
				edit: 'Editer',
				del: 'Supprimer la sélection',
				back: 'Retour',
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
		let options = {
			locale: 'fr',
			locales: locales,
			manipulation: {
				addNode: (nodeData, callback) => {
					if(this.handleNodeToAdd(nodeData)){
						callback(nodeData);
					}
					else{
						failAlert("Le champ choisi est vide !");
					}
				},
				editNode: (nodeData, callback) => {
					if (nodeData.id !== "start") {
						this.handleNodeToAdd(nodeData)
						callback(nodeData);
					} else{
						failAlert("Impossible de modifier le noeud de départ.");
						callback(null);
					}
				},
				deleteNode: (nodeData, callback) => {
					if (nodeData.nodes[0] !== "start") {
						callback(nodeData);
					} else{
						failAlert("Impossible de supprimer le noeud de départ.");
						callback(null);
					}
				},
				addEdge: (edgeData, callback) => {
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
		this.network = new vis.Network(container, data, options);
		this.network.focus("start");
	},

	/**
	* Check if all nodes have at least one parent node
	* @return {boolean}
	*/
	graphIsValid: function() {
		return this.nodes.get().filter((n) => {
			return n.id != "start"
		}).every((n1) => {
			return this.edges.get().some((e) => {
				return e.to == n1.id;
			})
		});
	},

	/**
	* Update the form to display the options corresponding to the type of button chosen
	*/
	updateForm: function() {
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
	},

	/**
	* Create a specific node corresponding to the option chosen
	* @param {Object} nodeData the data of the node to add
	* @return {boolean}
	*/
	handleNodeToAdd: function(nodeData) {
		let label = "";
		let action = {};
		nodeData.shape = 'box';
		if ($("#motionChoice").prop("checked") == true) {
			label += "motion:" + $("#left").val() + "," + $("#right").val();
			action.type = "motion";
			action.left = $("#left").val();
			action.right = $("#right").val();
		} else if ($("#servoChoice").prop("checked") == true) {
			label += "servo:" + $("#sequence").val();
			action.type = "servo";
			action.sequence = $("#sequence").val();
		} else if ($("#relayChoice").prop("checked") == true) {
			if($("#relay").val() == null)
				return false;
			label += "relay:" + $("#relay").val()+","+($("#relayOnOff").prop("checked")?1:0);
			action.type = "relay";
			action.relay = $("#relay").val();
			action.state = ($("#relayOnOff").prop("checked")?1:0)
		} else if ($("#speechChoice").prop("checked") == true) {
			label += "speech:\'" + $("#sentence").val() + "\'";
			action.type = "speech";
			action.speech = $("#sentence").val();
		} else if ($("#scriptChoice").prop("checked") == true) {
			if($("#script").val() == null)
				return false;
			label += "script:" + $("#script").val();
			action.type = "script";
			action.script = $("#script").val();
		} else if ($("#soundChoice").prop("checked") == true) {
			if($("#sound").val() == null)
				return false;
			label += "sound:" + $("#sound").val();
			action.type = "sound";
			action.sound = $("#sound").val();
		} else if ($("#pauseChoice").prop("checked") == true) {
			label += "pause:" + $("#pause").val() + "ms";
			nodeData.shape = "circle"
			action.type = "pause";
			action.time = $("#pause").val();
		}
		nodeData.label = label;
		nodeData.action = action;
		return true;
	}

}
