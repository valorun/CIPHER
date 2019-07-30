var templateController = (() => {
	'use strict';
	
	let DOM = {};
	let accordions = [];

	let openEvent = new CustomEvent('open', {bubbles: true, cancelable: true});
	let closeEvent = new CustomEvent('close', {bubbles: true, cancelable: true});
	

	/**
	 * Class used to represent the accordions containers in the page.
	 */
	class Accordion {
		/**
		 * Instanciate the accordion
		 * @param {*} $header header element with class 'accordion-header'
		 */
		constructor($header){
			this.$element = $header.parentNode;
			this.$content = this.$element.getElementsByClassName('accordion-content')[0];
			this.$icon = this.$element.getElementsByClassName('accordion-icon')[0];
			this.$icon.classList.add('fas', 'fa-angle-right');
			this.$icon.classList.remove('fa-angle-down');
			this.$content.style.display = 'none';

			$header.addEventListener('click', () =>{
				if (this.isOpen)
					this.close();
				else
					this.open();	
			});
		}

		open() {
			this.$icon.classList.add('fa-angle-down');
			this.$icon.classList.remove('fa-angle-right');
			this.$content.style.display = 'block';
			this.$element.dispatchEvent(openEvent);
		}

		close() {
			this.$icon.classList.add('fa-angle-right');
			this.$icon.classList.remove('fa-angle-down');
			this.$content.style.display = 'none';
			this.$element.dispatchEvent(closeEvent);
		}

		get isOpen() {
			return this.$content.style.display !== 'none';
		}

	}
	
	function init() {
		cacheDom();
		bindUIEvents();
	}

	function bindUIEvents() {
		document.getElementById('sidebar_button').addEventListener('click', () =>{
			if (isVisible(sidebar))
				close_sidebar();
			else
				open_sidebar();
		});

		document.getElementById('close_sidebar_button').addEventListener('click', () =>{
			close_sidebar();
		});

		document.getElementById('overlay').addEventListener('click', () =>{
			close_sidebar();
		});

		//setup collapse on accordions
		Array.from(document.getElementsByClassName('accordion-header')).forEach($header => 
			accordions.push(new Accordion($header))
		);
	}

	function cacheDom() {
		DOM.$sidebar = document.getElementById('sidebar');
		DOM.$overlayBg = document.getElementById('overlay');
	}

	function open_sidebar() {
		DOM.$sidebar.style.display = 'block';
		DOM.$overlayBg.style.display = 'block';
	}

	function close_sidebar() {
		DOM.$sidebar.style.display = 'none';
		DOM.$overlayBg.style.display = 'none';
	}

	return {
		init: init
	}

})();