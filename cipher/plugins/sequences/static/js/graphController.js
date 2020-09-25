/* globals failAlert */
/* globals vis */
/* globals ActionNode */
/* globals fetchJson */

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
      return n.id !== 'start';
    }).every((n1) => {
      return edges.get().some((e) => {
        return e.to === n1.id;
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
    _updateGraph(json, 'start');
    network.focus('start');
  }

  function _updateGraph(json, startId) {
    // add the nodes to the graph and create transitions for first ones
    if (json != null) {
      json.forEach(t => {
        const node = addActionNode(t.target);
        addTransition(startId, node.id, t.time);
        _updateGraph(t.target.transitions, node.id);
      });
    }
  }

  /**
   * Get graph as JSON.
   */
  function getGraph(startId = 'start') {
    return edges.get().filter(e => e.from === startId).map(e => {
      const transitionData = e.data;
      transitionData.target.action.transitions = getGraph(transitionData.target.id);
      transitionData.target = transitionData.target.action;

      return transitionData;
    });
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
          handleNodeToAdd(nodeData);
          resetMode();
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
          enabled: false,
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
    network.on('deselectEdge', () => DOM.$delSelectionButton.classList.add('hide'));

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

    DOM.$delSelectionButton.addEventListener('click', () => {
      network.deleteSelected();
      resetMode();
    });
  }

  function cacheDom() {
    DOM.$networkContainer = document.getElementById('network');
    DOM.$newNodeForm = document.getElementById('newNodeForm');
    DOM.$newTransitionForm = document.getElementById('newTransitionForm');

    DOM.$addNodeButton = document.getElementById('addNodeButton');
    DOM.$addTransitionButton = document.getElementById('addTransitionButton');
    DOM.$delSelectionButton = document.getElementById('delSelectionButton');

    DOM.$selectedAction = document.querySelector('select[name=newNodeTypeChoice]');

    DOM.$transitionTime = document.getElementById('transition_time');
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
    DOM.$newTransitionForm.classList.remove('hide');
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
    DOM.$newTransitionForm.classList.add('hide');
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
  function addTransition(fromId, toId, time) {
    const targetNode = nodes.get().find(n => n.id === toId);
    const edge = {
      from: fromId,
      to: toId,
      arrows: 'to',
      label: time + 'ms',
      data: { time: time, target: targetNode }
    };
    edges.add([edge]);
    return edge;
  }

  /**
   * Create an edge and check if it is correct.
   * @param {Object} edgeData the data of the node to add.
   * @return {Object} the new transition between the nodes.
   */
  function handleEdgeToAdd(edgeData) {
    const time = parseInt(DOM.$transitionTime.value);
    if (edgeData.from === edgeData.to || edgeData.to === 'start') {
      return;
    }
    return addTransition(edgeData.from, edgeData.to, time);
  }

  /**
   * Create a specific node corresponding to the options chosen
   */
  function handleNodeToAdd() {
    const action = {};
    action.name = DOM.$selectedAction.value;
    action.parameters = {};

    const $parameters = document.querySelectorAll('[id^=' + action.name + '_]:not([id$=_options])');
    $parameters.forEach(e => {
      const key = e.id.split(action.name + '_')[1];
      if (e.type === 'number') {
        action.parameters[key] = parseInt(e.value);
      } else if (e.type === 'checkbox') {
        action.parameters[key] = (e.checked ? 1 : 0);
      } else {
        action.parameters[key] = e.value;
      }
    });
    fetchJson('/check_action_parameters', 'POST', { action_name: action.name, parameters: action.parameters }).then(validation => {
      if (!validation[0]) {
        throw new TypeError(validation[1]);
      }
      addActionNode(action);
    }).catch(error => {
      console.error(error);
      failAlert(error.message);
    });
  }

  /**
   * Update the form to display the options corresponding to the type of button chosen
   */
  function updateForm() {
    document.querySelectorAll('[id$=_options]')
      .forEach(e => e.classList.add('hide'));

    if (document.querySelector('select[name=newNodeTypeChoice]').value !== '') {
      const selectedNodeType = document.querySelector('select[name=newNodeTypeChoice]');
      const selectedNodeForm = document.getElementById(selectedNodeType.value + '_options');
      if (selectedNodeForm != null) {
        selectedNodeForm.classList.remove('hide');
      }
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
