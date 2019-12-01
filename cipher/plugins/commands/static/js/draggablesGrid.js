'use strict';


/* exported DraggablesGrid */
class DraggablesGrid {
	
	constructor($grid_element, $trash_element){
		this.$grid_element = $grid_element;
		this.$trash_element = $trash_element;
		this.$cells = [];
		
		this.$trash_element.addEventListener('dragover', (e) => {
			e.preventDefault();
		});
		this.$trash_element.addEventListener('drop', (e) => {
			e.preventDefault();
			const data = e.dataTransfer.getData('text');
			const $to_del = document.getElementById(data);
			//DraggablesGrid.deleteEvent.detail = {target: $to_del};
			this.$grid_element.dispatchEvent(new CustomEvent('delete', {target: $to_del, bubbles: true, cancelable: true}));
			$to_del.parentNode.removeChild($to_del);
		});
	}

	addCell() {
		const $newCell = document.createElement('div');
		$newCell.classList.add('grid-cell');
		$newCell.addEventListener('drop', (e) => {
			e.preventDefault();
			const data = e.dataTransfer.getData('text');
			e.target.appendChild(document.getElementById(data));
		});
		$newCell.addEventListener('dragover', (e) => {
			e.preventDefault();
		});
		this.$grid_element.insertAdjacentElement('beforeend', $newCell);
		this.$cells.push($newCell);
		return this;
	}

	addCells(nb) {
		for (let i=0; i<nb; i++) {
			this.addCell();
		}
		return this;
	}

	addDraggableElement($el, index = 0) {
		let $inserted = null;
		let i = index;
		//const cells = document.getElementsByClassName('grid-cell');
		while ($inserted === null && i < this.$cells.length) {
			if ( this.$cells[i].firstChild === null) {
				$inserted = this.$cells[i].insertAdjacentElement('beforeend', $el);
				$inserted.addEventListener('dragstart', (e) => {
					e.dataTransfer.setData('text', e.target.id);
				});
				
				$inserted.draggable = false;
			}
			i++;
		}
		if ($inserted === null)
			throw new RangeError('Grid is full');

		return this;
	}

	enableDrag() {
		this.$cells.forEach(c => {
			c.style.border = '1px solid black';
		});
		this.draggables.forEach(d => d.element.draggable = true);
	}

	disableDrag() {
		this.$cells.forEach(c => {
			c.style.border = '';
		});
		this.draggables.forEach(d => d.element.draggable = false);
	}

	clearDraggables() {
		this.draggables.forEach((i, e) => {
			e.remove();
		});
	}

	get draggables() {
		return this.$cells.map((c, i) => {
			if(c.firstChild !== null)
				return {
					index: i,
					element: c.firstChild
				};
			else return null;
		}).filter(c => c !== null);
	}

}