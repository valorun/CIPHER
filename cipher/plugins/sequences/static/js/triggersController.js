/* globals fetchJson */

/* exported triggersController */
const triggersController = (() => {
  'use strict';

  const DOM = {};

  /* PUBLIC METHODS */
  function init() {
    cacheDom();
    bindUIEvents();
  }

  /* PRIVATE METHODS */
  function bindUIEvents() {
    document.querySelectorAll('input[name=enable-trigger]').forEach((e) => {
      const [,, triggerName, seqId] = e.id.split('-');
      e.addEventListener('click', () => {
        enableTrigger(triggerName, seqId, e.checked);
      });
    });
    document.querySelectorAll('button[name=delete-trigger]').forEach((e) => {
      const [,, triggerName, seqId] = e.id.split('-');
      e.addEventListener('click', () => {
        deleteSequence(triggerName, seqId);
      });
    });

    document.getElementById('link-trigger-button').addEventListener('click', () => {
      linkTrigger();
    });
  }

  function cacheDom() {
    DOM.$newTriggerName = document.getElementById('new-trigger-name');
    DOM.$newTriggerSequence = document.getElementById('new-trigger-sequence');
  }

  /**
   * Enable OR disable a trigger
   * @param {string} triggerName the name of the trigger to enable or disable
   * @param {string} seqId the ID of the sequence linked to the trigger to enable or disable
   * @param {boolean} value the new state for the trigger
   */
  function enableTrigger(triggerName, seqId, value) {
    fetchJson('/enable_trigger', 'POST', { trigger_name: triggerName, sequence_id: seqId, value: value })
      .then(() => {
        console.log('Trigger ' + triggerName + ' for sequence ' + seqId + ' updated');
      });
  }

  /**
   * Completely delete a trigger
   * @param {string} triggerName the name of the trigger to delete
   * @param {string} seqId the ID of the trigger to delete
   */
  function deleteSequence(triggerName, seqId) {
    const confirm = window.confirm('Etes vous sûr de vouloir supprimer le déclencheur \'' + triggerName + '-' + seqId + '\' ?');

    if (confirm) {
      fetchJson('/delete_trigger', 'POST', { trigger_name: triggerName, sequence_id: seqId })
        .then(() => {
          console.log('Trigger ' + triggerName + ' for sequence ' + seqId + ' deleted');
          const $seqEl = document.getElementById('trigger-' + triggerName + '-' + seqId);
          $seqEl.parentNode.removeChild($seqEl);
        });
    }
  }

  /**
   * Link a trigger to a sequence
   * @param {boolean} overwrite
   */
  function linkTrigger(overwrite = false) {
    fetchJson('/save_trigger', 'POST', { trigger_name: DOM.$newTriggerName.value, sequence_id: DOM.$newTriggerSequence.value, overwrite: overwrite })
      .then(() => {
        location.reload();
      }).catch(e => {
        if (e.code === 409) {
          const confirm = window.confirm('Une séquence portant le même nom existe déjà, voulez vous l\'écraser ?');
          if (confirm) {
            linkTrigger(true);
          }
        }
      });
  }
  return {
    init: init
  };
})();
