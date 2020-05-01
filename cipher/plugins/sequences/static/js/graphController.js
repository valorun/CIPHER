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
    font: { face: 'Electrolize' }
  };

  let nodes = null;
  let edges = null;
  let network = null;
  const ModeEnum = Object.freeze({ none: 0, addNode: 1, addTransition: 2 });
  let mode = ModeEnum.none;

  /* PUBLIC METHODS */
  function init() {
    cacheDom();
    bindUIEvents();
    updateForm();
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

  /* PRIVATE METHODS */
  function bindUIEvents() {
    document.getElementById('creation').addEventListener('open', () => {
      network.focus('start');
    });
    // create an array with nodes
    nodes = new vis.DataSet();
    nodes.add([START_NODE]);

    // create an array with edges
    edges = new vis.DataSet();

    // create a network
    const data = {
      nodes: nodes,
      edges: edges
    };
    const options = {
      locale: 'fr',
      manipulation: {
        enabled: false,
        addNode: (nodeData, callback) => {
          if (handleNodeToAdd(nodeData)) {
            callback(nodeData);
            resetMode();
          }
        },
        editNode: (nodeData, callback) => {
          if (nodeData.id !== 'start') {
            handleNodeToAdd(nodeData);
            callback(nodeData);
          } else {
            failAlert('Impossible de modifier le noeud de départ.');
            callback(null);
          }
        },
        deleteNode: (nodeData, callback) => {
          if (nodeData.nodes[0] !== 'start') {
            callback(nodeData);
          } else {
            failAlert('Impossible de supprimer le noeud de départ.');
            callback(null);
          }
        },
        addEdge: (edgeData, callback) => {
          if (handleEdgeToAdd(edgeData)) {
            callback(edgeData);
            enableAddTransitionMode();
          }
        },
        editEdge: (edgeData, callback) => {
          if (handleEdgeToAdd(edgeData)) {
            callback(edgeData);
          }
        }
      },
      layout: {
        hierarchical: {
          enabled: true,
          direction: 'DU',
          sortMethod: 'directed'
        },
        randomSeed: 2 // layout will be always the same
      }
    };
    network = new vis.Network(DOM.$networkContainer, data, options);
    network.focus('start');

    // show or hide the delete button according to the selection.
    network.on('selectNode', () => DOM.$delSelectionButton.classList.remove('hide'));
    network.on('selectEdge', () => DOM.$delSelectionButton.classList.remove('hide'));
    network.on('deselectNode', () => DOM.$delSelectionButton.classList.add('hide'));
    network.on('deselectNode', () => DOM.$delSelectionButton.classList.add('hide'));

    document.querySelector('select[name=newNodeTypeChoice]').addEventListener('change', () => {
      updateForm();
    });

    DOM.$addNodeButton.addEventListener('click', () => {
      if (mode === ModeEnum.addNode) {
        resetMode();
      } else {
        enableAddNodeMode();
      }
    });

    DOM.$addTransitionButton.addEventListener('click', () => {
      if (mode === ModeEnum.addTransition) {
        resetMode();
      } else {
        enableAddTransitionMode();
      }
    });

    DOM.$delSelectionButton.addEventListener('click', () => network.deleteSelected());
  }

  function cacheDom() {
    DOM.$networkContainer = document.getElementById('network');
    DOM.$newNodeForm = document.getElementById('newNodeForm');

    DOM.$addNodeButton = document.getElementById('addNodeButton');
    DOM.$addTransitionButton = document.getElementById('addTransitionButton');
    DOM.$delSelectionButton = document.getElementById('delSelectionButton');

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

    DOM.$motionOptions = document.getElementById('motionOptions');
    DOM.$servoOptions = document.getElementById('servoOptions');
    DOM.$relayOptions = document.getElementById('relayOptions');
    DOM.$speechOptions = document.getElementById('speechOptions');
    DOM.$scriptOptions = document.getElementById('scriptOptions');
    DOM.$soundOptions = document.getElementById('soundOptions');
    DOM.$pauseOptions = document.getElementById('pauseOptions');
    DOM.$servoSequenceOptions = document.getElementById('servoSequenceOptions');
  }

  /**
   * Disable other modes and allow user to add a new node.
   * Display a form allowing to select all informations for the new node.
   */
  function enableAddNodeMode() {
    resetMode();
    mode = ModeEnum.addNode;
    network.addNodeMode();
    DOM.$newNodeForm.classList.remove('hide');
    DOM.$addNodeButton.classList.add('disabled');
    DOM.$networkContainer.style.cursor = 'crosshair';
  }

  /**
   * Disable other modes and allow user to create a transition between two nodes.
   */
  function enableAddTransitionMode() {
    resetMode();
    mode = ModeEnum.addTransition;
    network.addEdgeMode();
    DOM.$addTransitionButton.classList.add('disabled');
    DOM.$networkContainer.style.cursor = 'crosshair';
  }

  /**
   * Disable all modes and hide all associated forms.
   */
  function resetMode() {
    mode = ModeEnum.none;
    network.disableEditMode();
    DOM.$newNodeForm.classList.add('hide');
    DOM.$addNodeButton.classList.remove('disabled');
    DOM.$addTransitionButton.classList.remove('disabled');
    DOM.$networkContainer.style.cursor = 'default';
  }

  /*
   * Manually add a new node in the graph.
   * @param {Object} action informations related to the new action node to add.
   * @return {ActionNode} the added action node.
   */
  function addActionNode(action) {
    const node = ActionNode.fromJSON(action);
    nodes.add([node]);
    return node;
  }

  /*
   * Manually add a new transition between two nodes.
   * @param {string} fromId the source node id.
   * @param {string} toId the target node id.
   * @return {Object} the new transition between the nodes.
   */
  function addTransition(fromId, toId) {
    const edge = { from: fromId, to: toId };
    edges.add([edge]);
    return edge;
  }

  /**
   * Create an edge and check if it is correct.
   * @param {Object} edgeData the data of the node to add
   * @return {boolean} false if the options aren't correct
   */
  function handleEdgeToAdd(edgeData) {
    edgeData.arrows = 'to';
    if (edgeData.from === edgeData.to || edgeData.to === 'start') {
      return false;
    }
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
        const $selectedServo = DOM.$servo.options[DOM.$servo.selectedIndex];
        action.servo = $selectedServo.value;
        action.position = parseInt(DOM.$servo_position.value);
        action.minPulseWidth = parseInt($selectedServo.dataset.min);
        action.maxPulseWidth = parseInt($selectedServo.dataset.max);
        action.speed = parseInt(DOM.$servo_speed.value);
        break;
      }
      case ('relay'): {
        action.relay = DOM.$relay.value;
        action.state = (DOM.$relay_on_off.checked ? 1 : 0);
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

  /**
   * Update the form to display the options corresponding to the type of button chosen
   */
  function updateForm() {
    DOM.$motionOptions.classList.add('hide');
    DOM.$servoOptions.classList.add('hide');
    DOM.$relayOptions.classList.add('hide');
    DOM.$speechOptions.classList.add('hide');
    DOM.$scriptOptions.classList.add('hide');
    DOM.$soundOptions.classList.add('hide');
    DOM.$pauseOptions.classList.add('hide');
    DOM.$servoSequenceOptions.classList.add('hide'); // COMPATIBILITY REASON
    if (document.querySelector('select[name=newNodeTypeChoice]').value !== '') {
      const selectedNodeType = document.querySelector('select[name=newNodeTypeChoice]');
      document.getElementById(selectedNodeType.value + 'Options').classList.remove('hide');
    } else {
      console.warn('Aucune action n\'a été selectionnée !');
    }
  }

  return {
    init: init,
    graphIsValid: graphIsValid,
    updateGraph: updateGraph,
    getGraph: getGraph
  };
})();
