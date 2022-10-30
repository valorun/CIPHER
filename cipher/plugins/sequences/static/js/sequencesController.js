/* globals graphController */
/* globals templateController */

/* globals failAlert */
/* globals fetchJson */

/* exported sequencesController */
const sequencesController = (() => {
  'use strict';

  const DOM = {};

  /* PUBLIC METHODS */
  function init() {
    cacheDom();
    bindUIEvents();
  }

  /* PRIVATE METHODS */
  function bindUIEvents() {
    document.querySelectorAll('input[name=enable-seq]').forEach((e) => {
      const [,, ...rest] = e.id.split('-');
      const seqName = rest.join('-');
      console.log(seqName)
      e.addEventListener('click', () => {
        enableSequence(seqName, e.checked);
      });
    });
    document.querySelectorAll('button[name=delete-seq]').forEach((e) => {
      const [,, ...rest] = e.id.split('-');
      const seqName = rest.join('-');
      e.addEventListener('click', () => {
        deleteSequence(seqName);
      });
    });
    document.querySelectorAll('button[name=edit-seq]').forEach((e) => {
      e.addEventListener('click', () => {
        const [,, ...rest] = e.id.split('-');
        const seqName = rest.join('-');

        editSequence(seqName);
        templateController.getAccordion('creation').open();
        window.location.hash = '#creation';
      });
    });

    document.getElementById('save-button').addEventListener('click', () => {
      if (graphController.graphIsValid()) {
        saveGraph();
      } else {
        failAlert('La séquence n\'est pas valide, certains noeuds n\'ont pas de parent.');
      }
    });
  }

  function cacheDom() {
    DOM.$name = document.getElementById('name');
  }

  /**
   * Enable OR disable a sequence
   * @param {string} seqName the name of the sequence to enable or disable
   * @param {boolean} value the new state for the sequence
   */
  function enableSequence(seqName, value) {
    fetchJson('/enable_sequence', 'POST', { seq_name: seqName, value: value })
      .then(() => {
        console.log('Sequence ' + seqName + ' updated');
      });
  }

  /**
   * Completely delete a sequence
   * @param {string} seqName the name of the sequence to delete
   */
  function deleteSequence(seqName) {
    const confirm = window.confirm('Etes vous sûr de vouloir supprimer la séquence \'' + seqName + '\' ?');

    if (confirm) {
      fetchJson('/delete_sequence', 'POST', { seq_name: seqName })
        .then(() => {
          console.log('Sequence ' + seqName + ' deleted');
          const $seqEl = document.getElementById('seq-' + seqName);
          $seqEl.parentNode.removeChild($seqEl);
        });
    }
  }

  /**
   * Edit the specified sequence
   * @param {string} seqName the name of the sequence to edit
   */
  function editSequence(seqName) {
    DOM.$name.value = seqName;
    const sequenceData = document.getElementById('data-seq-' + seqName).innerHTML;
    const json = JSON.parse(sequenceData);
    graphController.updateGraph(json);
  }

  /**
   * Save the graph on server
   * @param {boolean} overwrite
   */
  function saveGraph(overwrite = false) {
    const sequence = graphController.getGraph();
    fetchJson('/save_sequence', 'POST', { seq_name: DOM.$name.value, seq_data: sequence, seq_overwrite: overwrite })
      .then(() => {
        location.reload();
      }).catch(e => {
        if (e.code === 409) {
          const confirm = window.confirm('Une séquence portant le même nom existe déjà, voulez vous l\'écraser ?');
          if (confirm) {
            saveGraph(true);
          }
        }
      });
  }

  return {
    init: init
  };
})();
