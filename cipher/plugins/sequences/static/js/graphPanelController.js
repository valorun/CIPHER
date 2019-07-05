var graphPanelController = {
	nodes: null,
	edges: null,
	network: null,

	init: function(){
		this.bind();
		this.render();
	},
	bind: function(){
		$('#creation').on('open', () => {
			this.network.focus('start');
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
				},
				editNode: (nodeData, callback) => {
					if (nodeData.id !== 'start') {
						this.handleNodeToAdd(nodeData);
						callback(nodeData);
					} else{
						failAlert('Impossible de modifier le noeud de départ.');
						callback(null);
					}
				},
				deleteNode: (nodeData, callback) => {
					if (nodeData.nodes[0] !== 'start') {
						callback(nodeData);
					} else{
						failAlert('Impossible de supprimer le noeud de départ.');
						callback(null);
					}
				},
				addEdge: (edgeData, callback) => {
					if(this.handleEdgeToAdd(edgeData))
						callback(edgeData);
				},
				editEdge: (edgeData, callback) => {
					if(this.handleEdgeToAdd(edgeData))
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
		this.network.focus('start');
	},

	/**
	* Check if all nodes have at least one parent node
	* @return {boolean}
	*/
	graphIsValid: function() {
		return this.nodes.get().filter((n) => {
			return n.id != 'start';
		}).every((n1) => {
			return this.edges.get().some((e) => {
				return e.to == n1.id;
			});
		});
	},

	/**
	* Create an edge and check if it is correct.
	* @param {Object} edgeData the data of the node to add
	* @return {boolean} false if the options aren't correct
	*/
	handleEdgeToAdd: function(edgeData) {
		edgeData.arrows = 'to';
		if(edgeData.from === edgeData.to)
			return false;
		
		return true;

	},


	/**
	* Create a specific node corresponding to the options chosen
	* @param {Object} nodeData the data of the node to add
	* @return {boolean} false if the options aren't correct
	*/
	handleNodeToAdd: function(nodeData) {
		let label = '';
		let action = {};
		let selectedAction = $('select[name=newNodeTypeChoice]').val();
		nodeData.shape = 'box';
		if (selectedAction == 'motion') {
			action.type = 'motion';
			action.direction = $('#motion_direction').val();
			if(action.direction == null){
				failAlert('Aucune direction sélectionnée.');
				return false;
			}
			action.speed = parseInt($('#motion_speed').val());
			if(!this.isInputNumberValid(action.speed, 0, 100)){
				failAlert('La vitesse doit être comprise entre 0 et 100.');
				return false;
			}
			label += 'motion:' + action.direction + ',' + action.speed;
		} else if (selectedAction == 'servo') {
			action.type = 'servo';
			action.servo = $('#servo').val();
			if(action.servo == null){
				failAlert('Aucun servomoteur sélectionné.');
				return false;
			}
			action.position = parseInt($('#servo_position').val());
			let min_pulse_width = parseInt($('#servo option:selected').data('min'));
			let max_pulse_width = parseInt($('#servo option:selected').data('max'));
			if(!this.isInputNumberValid(action.position, min_pulse_width, max_pulse_width)){
				failAlert('La position doit être comprise entre ' + min_pulse_width + ' et ' + max_pulse_width + '.');
				return false;
			}
			action.speed = parseInt($('#servo_speed').val());
			if(!this.isInputNumberValid(action.speed, 0, 100)){
				failAlert('La vitesse doit être comprise entre 0 et 100.');
				return false;
			}
			label += 'servo:' + action.servo + ',' + action.position + ',' + action.speed;
		} else if (selectedAction == 'relay') {
			action.type = 'relay';
			action.relay = $('#relay').val();
			if(action.relay == null){
				failAlert('Aucun relai sélectionné.');
				return false;
			}
			action.state = ($('#relayOnOff').prop('checked')?1:0);
			label += 'relay:' + action.relay + ',' + action.state;
		} else if (selectedAction == 'speech') {
			action.type = 'speech';
			action.speech = $('#sentence').val();
			label += 'speech:\'' + action.speech + '\'';
		} else if (selectedAction == 'script') {
			action.type = 'script';
			action.script = $('#script').val();
			if(action.script == null){
				failAlert('Aucun script sélectionné.');
				return false;
			}
			label += 'script:' + action.script;
		} else if (selectedAction == 'sound') {
			action.type = 'sound';
			action.sound = $('#sound').val();
			if(action.sound == null){
				failAlert('Aucun son sélectionné.');
				return false;
			}
			label += 'sound:' + action.sound;
		} else if (selectedAction == 'pause') {
			nodeData.shape = 'circle';
			action.type = 'pause';
			action.time = parseInt($('#pause').val());
			label += 'pause:' + action.time + 'ms';
		} else if (selectedAction == 'servoSequence'){ //COMPATIBILITY REASON
			action.type = 'servo_sequence';
			action.sequence = parseInt($('#sequence').val());
			nodeData.shape = 'circle';
			label += 'servo_sequence:' + action.sequence;
		} else
			return false;
		nodeData.label = label;
		nodeData.action = action;
		return true;
	},

	isInputNumberValid: function(value, min, max){
		return !isNaN(parseInt(value)) && value <= max && value >= min;
	}
};
