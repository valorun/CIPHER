/* globals fetchJson */

/* exported sequencesController */
const sequencesController = (() => {
	'use strict';

	/* PUBLIC METHODS */
	function init(){
		bindUIEvents();
	}

	/* PRIVATE METHODS */
	function bindUIEvents() {

		document.querySelectorAll('input[name=enableSeq]').forEach((e) => {
			const seq_name = e.id.substring(e.id.indexOf('_') + 1);
			e.addEventListener('click', () => {
				enableSequence(seq_name, e.checked);
			});
		});
		document.querySelectorAll('a[name=deleteSeq]').forEach((e) => {
			const seq_name = e.id.substring(e.id.indexOf('_') + 1);
			e.addEventListener('click', () => {
				deleteSequence(seq_name);
			});
		});
	}

	/**
	* Enable OR disable a sequence
	* @param {string} seq_name the name of the sequence to enable or disable
	* @param {boolean} value the new state for the sequence
	*/
	function enableSequence(seq_name, value){
		fetchJson('/enable_sequence', 'POST', {seq_name:seq_name, value:value})
			.then(()=> {
				console.log(seq_name + ' updated');
			});
	}

	/**
	* Completely delete a sequence
	* @param {string} seq_name the name of the sequence to delete
	*/
	function deleteSequence(seq_name){
		const confirm = window.confirm('Etes vous sûr de vouloir supprimer la séquence \'' + seq_name + '\' ?');
		
		if(confirm){
			fetchJson('/delete_sequence', 'POST', {seq_name:seq_name})
				.then(()=> {
					console.log(seq_name + ' deleted');
					const $seq_el = document.getElementById(seq_name);
					$seq_el.parentNode.removeChild($seq_el);
				});
		}
	}

	return {
		init: init
	};
})();
