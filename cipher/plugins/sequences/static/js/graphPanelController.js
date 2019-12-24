/* globals failAlert */
/* globals vis */

/* exported graphPanelController */
const graphPanelController = (() => {
	'use strict';

	const DOM = {};

	let nodes = null;
	let edges = null;
	let network = null;

	/* PUBLIC METHODS */
	function init(){
		cacheDom();
		bindUIEvents();
	}

	/**
	* Check if all nodes have at least one parent node
	* @return {boolean}
	*/
	function graphIsValid() {
		return nodes.get().filter((n) => {
			return n.id != 'start';
		}).every((n1) => {
			return edges.get().some((e) => {
				return e.to == n1.id;
			});
		});
	}

	/**
	 * Update nodes and edges of the graph.
	 * @param {*} n Nodes in JSON.
	 * @param {*} e Edges in JSON.
	 */
	function updateGraph(n, e) {
		nodes.clear();
		edges.clear();
		nodes.update(n);
		edges.update(e);
		network.focus('start');
	}

	/**
	 * Get graph as JSON.
	 */
	function getGraph() {
		const graph = {};
		graph.nodes = nodes.get();
		graph.edges = edges.get();
		return graph;
	}

	/* PRIVATE METHODS */
	function bindUIEvents(){
		document.getElementById('creation').addEventListener('open', () => {
			network.focus('start');
		});
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
		const container = document.getElementById('network');
		const data = {
			nodes: nodes,
			edges: edges
		};
		const locales = {
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
		const options = {
			locale: 'fr',
			locales: locales,
			manipulation: {
				addNode: (nodeData, callback) => {
					if(handleNodeToAdd(nodeData)){
						callback(nodeData);
					}
				},
				editNode: (nodeData, callback) => {
					if (nodeData.id !== 'start') {
						handleNodeToAdd(nodeData);
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
					if(handleEdgeToAdd(edgeData))
						callback(edgeData);
				},
				editEdge: (edgeData, callback) => {
					if(handleEdgeToAdd(edgeData))
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
		network.focus('start');
	}

	function cacheDom() {
		DOM.$selectedAction = document.querySelector('select[name=newNodeTypeChoice]');

		DOM.$motion_direction = document.getElementById('motion_direction');
		DOM.$motion_speed = document.getElementById('motion_speed');

		DOM.$servo = document.getElementById('servo');
		DOM.$servo_position = document.getElementById('servo_position');
		DOM.$servo_speed = document.getElementById('servo_speed');

		DOM.$relay = document.getElementById('relay');
		DOM.$relay_on_off = document.getElementById('relay_on_off');

		DOM.$speech_sentence = document.getElementById('speech_sentence');

		DOM.$script_name = document.getElementById('script_name');

		DOM.$sound_name = document.getElementById('sound_name');

		DOM.$pause = document.getElementById('pause');

		DOM.$servo_sequence = document.getElementById('servo_sequence');

	}

	/**
	* Create an edge and check if it is correct.
	* @param {Object} edgeData the data of the node to add
	* @return {boolean} false if the options aren't correct
	*/
	function handleEdgeToAdd(edgeData) {
		edgeData.arrows = 'to';
		if(edgeData.from === edgeData.to || edgeData.to === 'start')
			return false;
		
		return true;
	}

	/**
	* Create a specific node corresponding to the options chosen
	* @param {Object} nodeData the data of the node to add
	* @return {boolean} false if the options aren't correct
	*/
	function handleNodeToAdd(nodeData) {
		let label = '';
		const action = {};
		nodeData.shape = 'box';
		nodeData.font = {};
		nodeData.font.face = 'Electrolize';
		action.type = DOM.$selectedAction.value;
		switch (DOM.$selectedAction.value) {
		case ('motion'): {
			action.direction = DOM.$motion_direction.value;
			if(action.direction == null || action.direction === ''){
				failAlert('Aucune direction sélectionnée.');
				return false;
			}
			action.speed = parseInt(DOM.$motion_speed.value);
			if(!isInputNumberValid(action.speed, 0, 100)){
				failAlert('La vitesse doit être comprise entre 0 et 100.');
				return false;
			}
			label += 'motion:' + action.direction + ',' + action.speed;
			break;
		}
		case ('servo'): {
			const $selected_servo = DOM.$servo.options[DOM.$servo.selectedIndex];
			action.servo = $selected_servo.value;
			if(action.servo == null || action.servo === ''){
				failAlert('Aucun servomoteur sélectionné.');
				return false;
			}
			action.position = parseInt(DOM.$servo_position.value);
			const min_pulse_width = parseInt($selected_servo.dataset.min);
			const max_pulse_width = parseInt($selected_servo.dataset.max);
			if(!isInputNumberValid(action.position, min_pulse_width, max_pulse_width)){
				failAlert('La position doit être comprise entre ' + min_pulse_width + ' et ' + max_pulse_width + '.');
				return false;
			}
			action.speed = parseInt(DOM.$servo_speed.value);
			if(!isInputNumberValid(action.speed, 0, 100)){
				failAlert('La vitesse doit être comprise entre 0 et 100.');
				return false;
			}
			label += 'servo:' + action.servo + ',' + action.position + ',' + action.speed;
			break;
		}
		case ('relay'): {
			action.relay = DOM.$relay.value;
			if(action.relay == null || action.relay === ''){
				failAlert('Aucun relai sélectionné.');
				return false;
			}
			action.state = (DOM.$relay_on_off.checked?1:0);
			label += 'relay:' + action.relay + ',' + action.state;
			break;
		}
		case ('speech'): {
			action.speech = DOM.$speech_sentence.value;
			label += 'speech:\'' + action.speech + '\'';
			break;
		}
		case ('script'): {
			action.script = DOM.$script_name.value;
			if(action.script == null || action.script === ''){
				failAlert('Aucun script sélectionné.');
				return false;
			}
			label += 'script:' + action.script;
			break;
		}
		case ('sound'): {
			action.sound = DOM.$sound_name.value;
			if(action.sound == null || action.sound === ''){
				failAlert('Aucun son sélectionné.');
				return false;
			}
			label += 'sound:' + action.sound;
			break;
		}
		case ('pause'): {
			nodeData.shape = 'circle';
			action.time = parseInt(DOM.$pause.value);
			label += 'pause:' + action.time + 'ms';
			break;
		}
		case ('servoSequence'): { // COMPATIBILITY REASON
			action.type = 'servo_sequence';
			action.sequence = parseInt(DOM.$servo_sequence.value);
			nodeData.shape = 'circle';
			label += 'servo_sequence:' + action.sequence;
			break;
		}
		default: {
			return false;
		}
		}
		nodeData.label = label;
		nodeData.action = action;
		return true;
	}

	function isInputNumberValid(value, min, max){
		return !isNaN(parseInt(value)) && value <= max && value >= min;
	}

	return {
		init: init,
		graphIsValid: graphIsValid,
		updateGraph: updateGraph,
		getGraph: getGraph
	};

})();
