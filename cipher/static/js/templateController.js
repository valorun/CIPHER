var templateController = (() => {
	let sidebar = null;
	let overlayBg = null;
	
	function init() {
		sidebar = $('#sidebar');
		overlayBg = $('#overlay');
		bind();
	}
	function bind() {
		$('#sidebar_button').on('click', () =>{
			if (this.sidebar.is(':visible'))
				this.close_sidebar();
			else
				this.open_sidebar();
		});
		$('#close_sidebar_button').on('click', () =>{
			this.close_sidebar();
		});
		$('#overlay').on('click', () =>{
			this.close_sidebar();
		});

		//setup collapse on accordions
		$('.accordion-header').each( (i, header) => {
			let element = $(header).parent();
			let content=element.find('.accordion-content');
			let icon=$(header).find('.accordion-icon');
			icon.addClass('fas fa-angle-right');
			icon.removeClass('fa-angle-down');
			content.hide();

			$(header).on('click', () =>{
				if(this.is_accordion_open(element))
					this.close_accordion(element);
				else
					this.open_accordion(element);	
			});
		});
	}

	/**
	* Open the specified accordion
	* @param {JQuery} e the accordion object
	*/
	function open_accordion(e) {
		let header=e.find('.accordion-header');
		let content=e.find('.accordion-content');
		let icon=header.find('.accordion-icon');
		icon.addClass('fa-angle-down');
		icon.removeClass('fa-angle-right');
		content.show();
		e.trigger('open');
	}

	/**
	* Close the specified accordion
	* @param {JQuery} e the accordion object
	*/
	function close_accordion(e) {
		let header=e.find('.accordion-header');
		let content=e.find('.accordion-content');
		let icon=header.find('.accordion-icon');
		icon.addClass('fa-angle-right');
		icon.removeClass('fa-angle-down');
		content.hide();
		e.trigger('close');
	}
	/**
	* Check id the specified accordion is open
	* @param {JQuery} e the accordion object
	* @returns {boolean}
	*/ 
	function is_accordion_open(e) {
		let content=e.find('.accordion-content');
		return content.is(':visible');
	}

	function open_sidebar() {
		this.sidebar.show();
		this.overlayBg.show();
	}

	function close_sidebar() {
		this.sidebar.hide();
		this.overlayBg.hide();
	}

})();