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
		$("#creation").on("open", () => {
			this.network.focus("start");
		});
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
		$("#conditionOptions").addClass("hide");
		if($('select[name=newNodeTypeChoice]').val()!==""){
			$("#" +$('select[name=newNodeTypeChoice]').val()+ "Options").removeClass("hide");
		}
		else{
			failAlert("Aucune action n'a été selectionnée !");
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
		let selectedAction = $('select[name=newNodeTypeChoice]').val();
		nodeData.shape = 'box';
		if (selectedAction == 'motion') {
			action.type = "motion";
			action.direction = $("#motion_direction").val();
			action.speed = $("#motion_speed").val();
			label += "motion:" + action.direction + "," + action.speed;
		} else if (selectedAction == 'servo') {
			action.servo = $("#servo").val();
			if(action.servo == null)
				return false;
			action.type = "servo";
			action.position = $("#servo_position").val();
			action.speed = $("#servo_speed").val();
			label += "servo:" + action.servo+","+action.position+","+action.speed;
		} else if (selectedAction == 'relay') {
			action.relay = $("#relay").val();
			if(action.relay == null)
				return false;
			action.type = "relay";
			action.state = ($("#relayOnOff").prop("checked")?1:0)
			label += "relay:" + action.relay+","+action.state;
		} else if (selectedAction == 'speech') {
			action.type = "speech";
			action.speech = $("#sentence").val();
			label += "speech:\'" + action.speech + "\'";
		} else if (selectedAction == 'script') {
			action.script = $("#script").val();
			if(action.script == null)
				return false;
			action.type = "script";
			label += "script:" + action.script;
		} else if (selectedAction == 'sound') {
			action.sound = $("#sound").val();
			if(action.sound == null)
				return false;
			action.type = "sound";
			label += "sound:" + action.sound;
		} else if (selectedAction == 'pause') {
			nodeData.shape = "circle"
			action.type = "pause";
			action.time = $("#pause").val();
			label += "pause:" + action.time + "ms";
		} else if (selectedAction == 'condition'){
			if($("#flag").val() == null)
				return false;
			if($("#flag").val().split(' ').length > 1){
				failAlert("Un seul drapeau peut être ajouté à la fois et ne doit pas contenir d'espaces.");
				return false;
			}
			nodeData.shape = "diamond"
			action.type = "condition";
			action.flag = $("#flag").val().split(' ')[0];
			label += "condition:" + action.flag;
		}
		nodeData.label = label;
		nodeData.action = action;
		return true;
	}

}
