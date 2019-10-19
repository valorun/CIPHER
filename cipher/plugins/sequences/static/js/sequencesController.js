/* globals failAlert */

/* exported sequencesController */
var sequencesController = (() => {
	'use strict';

	/* PUBLIC METHODS */
	function init(){
		bindUIEvents();
	}

	/* PRIVATE METHODS */
	function bindUIEvents() {

		document.querySelectorAll('input[name=enableSeq]').forEach((e) => {
			const seq_name = e.id.substr(e.id.indexOf('_') + 1);
			e.addEventListener('click', () => {
				enableSequence(seq_name, e.checked);
			});
		});
		document.querySelectorAll('a[name=deleteSeq]').forEach((e) => {
			const seq_name = e.id.substr(e.id.indexOf('_') + 1);
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
		let headers = new Headers();
		headers.append('Content-Type', 'application/json');
		fetch('/enable_sequence', {
			method: 'POST',
			headers: headers,
			body: JSON.stringify({seq_name:seq_name, value:value})
		})
			.then((response) => {
				if(response.status != 200) {
					response.json().then((r) => failAlert(r));
					return;
				}
				console.log(seq_name + ' updated');

			});
	}

	/**
	* Completely delete a sequence
	* @param {string} seq_name the name of the sequence to delete
	*/
	function deleteSequence(seq_name){
		let confirm = window.confirm('Etes vous sûr de vouloir supprimer la séquence \'' + seq_name + '\' ?');
		let headers = new Headers();
		headers.append('Content-Type', 'application/json');
		if(confirm){
			fetch('/delete_sequence', {
				method: 'POST',
				headers: headers,
				body: JSON.stringify({seq_name:seq_name})
			})
				.then((response) => {
					if(response.status != 200) {
						response.json().then((r) => failAlert(r));
						return;
					}
					console.log(seq_name + ' deleted');
					let seq_el = document.getElementById(seq_name);
					seq_el.parentNode.removeChild(seq_el);
				});
		}
	}

	return {
		init: init
	};
})();
