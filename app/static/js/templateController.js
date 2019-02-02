var templateController = {
	sidebar: null,
	overlayBg : null,

	init: function(){
		this.sidebar=$("#sidebar");
		this.overlayBg=$("#overlay");
		this.bind();
	},
	bind: function(){
		$("#sidebar_button").on("click", () =>{
			if (this.sidebar.is(":visible"))
				this.close_sidebar();
			else
				this.open_sidebar();
		});
		$("#close_sidebar_button").on("click", () =>{
			this.close_sidebar();
		});
		$("#overlay").on("click", () =>{
			this.close_sidebar();
		});

		//setup collapse on accordions
		$(".accordion-header").each( (i, e) => {
			let content=$(e).parent().find(".accordion-content");
			let icon=$(e).find(".accordion-icon");
			icon.addClass("fas fa-angle-right");
			icon.removeClass("fa-angle-down");
			content.hide();

			$(e).on("click", () =>{
				if(content.is(":visible")){
					icon.addClass("fa-angle-right");
					icon.removeClass("fa-angle-down");
					content.hide();
				}
				else{
					icon.addClass("fa-angle-down");
					icon.removeClass("fa-angle-right");
					content.show();
				}
			});

		});
	},

	open_sidebar: function() {
		this.sidebar.show();
		this.overlayBg.show();
	},

	close_sidebar: function() {
		this.sidebar.hide();
		this.overlayBg.hide();
	}

}
