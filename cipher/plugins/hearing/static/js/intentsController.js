/* globals failAlert */
/* globals fetchJson */

/* exported intentsController */
const intentsController = (() => {
  'use strict';

  const DOM = {};

  /* PUBLIC METHODS */
  function init() {
    cacheDom();
    bindUIEvents();
  }

  /* PRIVATE METHODS */
  function bindUIEvents() {
    // button to add the sentence to the conversation
    document.getElementById('add-response-button').addEventListener('click', () => {
      const intent = DOM.$currentIntent.value;
      if (intent == null || intent === '') {
        failAlert('L\'intention fournie est vide.');
        return;
      }
      const sequenceId = DOM.$currentSequence.value;
      const actionName = null;//DOM.$currentAction.value;
      saveIntent(intent, actionName, sequenceId);
    });

    // checkbox to enable or disable the relay
    document.querySelectorAll('button[name=enable-intent]').forEach((e) => {
      const intent = e.id.substring(e.id.indexOf('-') + 1);
      e.addEventListener('change', () => {
        enableIntent(intent, e.checked);
      });
    });

    // button to delete the relay
    document.querySelectorAll('button[name=delete-intent]').forEach((e) => {
      const intent = e.id.substring(e.id.indexOf('-') + 1);
      e.addEventListener('click', () => {
        deleteIntent(intent);
      });
    });
  }

  function cacheDom() {
    DOM.$currentIntent = document.getElementById('current-intent');
    DOM.$currentSequence = document.getElementById('current-sequence');
    DOM.$currentAction = document.getElementById('current-action');
  }

  /**
  * Save an intent
  * @param {*} intent intent name
  * @param {*} action_name optional action name
  * @param {*} sequence_id optional sequence id
  */
  function saveIntent(intent, actionName, sequenceId) {
    fetchJson('/save_intent', 'POST',
      { intent: intent, action_name: actionName, sequence_id: sequenceId })
      .then(() => {
        location.reload();
      });
  }

  /**
  * Enable OR disable an intent
  * @param {string} intent intent name
  * @param {boolean} value new state for the intent
  */
  function enableIntent(intent, value) {
    fetchJson('/enable_intent', 'POST', { intent: intent, value: value })
      .then(() => {
        console.log(intent + ' updated');
      });
  }

  /**
  * Delete an intent
  * @param {string} intent intent name
  */
  function deleteIntent(intent) {
    const confirm = window.confirm('Etes vous sûr de vouloir supprimer l\'intention \'' + intent + '\' ?');

    if (confirm) {
      fetchJson('/delete_intent', 'POST', { intent: intent })
        .then(() => {
          console.log(intent + ' deleted');
          const $intentEl = document.getElementById(intent);
          $intentEl.parentNode.removeChild($intentEl);
        });
    }
  }

  return {
    init: init
  };
})();
