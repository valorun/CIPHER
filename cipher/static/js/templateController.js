var templateController = {
	sidebar: null,
	overlayBg: null,
	openEvent: new CustomEvent('open', {bubbles: true, cancelable: true}),
	closeEvent: new CustomEvent('close', {bubbles: true, cancelable: true}),
	
	init: function(){
		this.sidebar = document.getElementById('sidebar');
		this.overlayBg = document.getElementById('overlay');
		this.bind();
	},
	bind: function(){
		document.getElementById('sidebar_button').addEventListener('click', () =>{
			if (isVisible(this.sidebar))
				this.close_sidebar();
			else
				this.open_sidebar();
		});
		document.getElementById('close_sidebar_button').addEventListener('click', () =>{
			this.close_sidebar();
		});
		document.getElementById('overlay').addEventListener('click', () =>{
			this.close_sidebar();
		});

		//setup collapse on accordions
		Array.from(document.getElementsByClassName('accordion-header')).forEach(header => {
			let element = header.parentNode;
			let content = element.getElementsByClassName('accordion-content')[0];
			let icon = element.getElementsByClassName('accordion-icon')[0];
			icon.classList.add('fas', 'fa-angle-right');
			icon.classList.remove('fa-angle-down');
			content.style.display = 'none';

			header.addEventListener('click', () =>{
				if(this.is_accordion_open(element))
					this.close_accordion(element);
				else
					this.open_accordion(element);	
			});
		});
	},

	/**
	* Open the specified accordion
	* @param {HTMLElement} e the accordion object
	*/
	open_accordion: function(e){
		let header = e.getElementsByClassName('accordion-header')[0];
		let content = e.getElementsByClassName('accordion-content')[0];
		let icon = header.getElementsByClassName('accordion-icon')[0];
		icon.classList.add('fa-angle-down');
		icon.classList.remove('fa-angle-right');
		content.style.display = 'block';
		e.dispatchEvent(this.openEvent);
	},

	/**
	* Close the specified accordion
	* @param {HTMLElement} e the accordion object
	*/
	close_accordion: function(e){
		let header = e.getElementsByClassName('accordion-header')[0];
		let content = e.getElementsByClassName('accordion-content')[0];
		let icon = header.getElementsByClassName('accordion-icon')[0];
		icon.classList.add('fa-angle-right');
		icon.classList.remove('fa-angle-down');
		content.style.display = 'none';
		e.dispatchEvent(this.closeEvent);
	},
	/**
	* Check id the specified accordion is open
	* @param {HTMLElement} e the accordion object
	* @returns {boolean}
	*/ 
	is_accordion_open: function(e){
		let content = e.getElementsByClassName('accordion-content')[0];
		return content.style.display !== 'none';
	},

	open_sidebar: function() {
		this.sidebar.style.display = 'block';
		this.overlayBg.style.display = 'block';
	},

	close_sidebar: function() {
		this.sidebar.style.display = 'none';
		this.overlayBg.style.display = 'none';
	}

};