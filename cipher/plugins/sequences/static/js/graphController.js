/* globals failAlert */
/* globals vis */
/* globals ActionNode */

/* exported graphController */
const graphController = (() => {
	'use strict';

	const DOM = {};

	const START_NODE = {
		id: 'start',
		title: 'Start',
		color: 'red',
		shape: 'circle',
		font: {face: 'Electrolize'}
	};

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
	 * @param {*} jsonNodes The graph in JSON.
	 */
	function updateGraph(json) {
		nodes.clear();
		edges.clear();
		
		nodes.add([START_NODE]);
		
		// add the nodes to the graph and create transitions for first ones
		_updateGraph(json).forEach(c => addTransition('start', c.id));
		network.focus('start');
	}

	function _updateGraph(json) {
		const nodes = [];
		json.forEach(a => {
			const node = addActionNode(a);
			nodes.push(node);
			const children = _updateGraph(a.children);
			children.forEach(c => addTransition(node.id, c.id));
		});
		// return added nodes that will became children in next iteration
		return nodes;
	}

	/**
	 * Get graph as JSON.
	 */
	function getGraph(nodesData = null) {
		if (nodesData === null) {
			nodesData = [];
			// get start node childrens
			nodesData = nodes.get().filter(n => edges.get().filter(e => e.from === 'start' && e.to === n.id).length > 0);
		}

		const graph = nodesData.map(n => {
			const node = n.action;
			const children = nodes.get().filter(n1 => edges.get().filter(e => e.from === n.id && e.to === n1.id).length > 0);
			node.children = getGraph(children);
			return node;
		});

		return graph;
	}
	
	function addActionNode(action) {
		const node = ActionNode.fromJSON(action);
		nodes.add([node]);
		return node;
	}

	function addTransition(fromId, toId) {
		const edge = {'from': fromId, 'to': toId};
		edges.add([edge]);
		return edge;
	}

	/* PRIVATE METHODS */
	function bindUIEvents(){
		document.getElementById('creation').addEventListener('open', () => {
			network.focus('start');
		});
		// create an array with nodes
		nodes = new vis.DataSet();
		nodes.add([START_NODE]);

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
		const action = {};
		action.type = DOM.$selectedAction.value;
		switch (DOM.$selectedAction.value) {
		case ('motion'): {
			action.direction = DOM.$motion_direction.value;
			action.speed = parseInt(DOM.$motion_speed.value);
			break;
		}
		case ('servo'): {
			const $selected_servo = DOM.$servo.options[DOM.$servo.selectedIndex];
			action.servo = $selected_servo.value;
			action.position = parseInt(DOM.$servo_position.value);
			action.minPulseWidth = parseInt($selected_servo.dataset.min);
			action.maxPulseWidth = parseInt($selected_servo.dataset.max);
			action.speed = parseInt(DOM.$servo_speed.value);
			break;
		}
		case ('relay'): {
			action.relay = DOM.$relay.value;
			action.state = (DOM.$relay_on_off.checked?1:0);
			break;
		}
		case ('speech'): {
			action.speech = DOM.$speech_sentence.value;
			break;
		}
		case ('script'): {
			action.script = DOM.$script_name.value;
			break;
		}
		case ('sound'): {
			action.sound = DOM.$sound_name.value;
			break;
		}
		case ('pause'): {
			nodeData.shape = 'circle';
			action.time = parseInt(DOM.$pause.value);
			break;
		}
		case ('servoSequence'): { // COMPATIBILITY REASON
			action.sequence = parseInt(DOM.$servo_sequence.value);
			break;
		}
		default: {
			return false;
		}
		}
		try {
			Object.assign(nodeData, ActionNode.fromJSON(action));
			return true;
		} catch (error) {
			console.error(error);
			failAlert(error.message);
		}
		return false;
	}


	return {
		init: init,
		graphIsValid: graphIsValid,
		updateGraph: updateGraph,
		getGraph: getGraph
	};

})();
