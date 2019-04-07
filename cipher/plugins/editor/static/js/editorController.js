var editorController = {
	editor: null,
	init: function(){
		this.editor = ace.edit("editor", {
			theme: "ace/theme/twilight",
			mode: "ace/mode/python",
			selectionStyle: "text"
		});
		this.bind();
	},
	bind: function(){
		$('a[name=editScript]').on("click", (e) => {
			let script_name=e.currentTarget.id.substr(e.currentTarget.id.indexOf('_')+1);
			this.editScript(script_name)
		});
		$('a[name=deleteScript]').on("click", (e) => {
			//get the sequence name by getting the second part of the id, after '_'
			let script_name=e.currentTarget.id.substr(e.currentTarget.id.indexOf('_')+1)
			this.deleteScript(script_name)
		});
		$('#saveButton').on("click", (e) => {
			this.saveScript($('#name').val(), this.editor.getValue());
		});
	},

	/**
	 * Edit the specified script
	 * @param {string} script_name the name of the script to edit
	 */
	editScript: function(script_name){
		$("#name").val(script_name);
		editor = this.editor;
		$.ajax({
			type: 'GET',
			url: '/read_script/' + script_name,
			success: function(data){
				editor.setValue(data)
				templateController.open_accordion($("#editorPanel"));
				window.location.hash = '#editorPanel';
			},
			error: function(request, status, error){
				failAlert(request.responseText);
			}
		});
	},

	/**
	 * Completely delete a script
	 * @param {string} script_name the name of the script to delete
	 */
	deleteScript: function(script_name){
		let confirm = window.confirm("Etes vous sûr de vouloir supprimer le script \'"+script_name+"\' ?");
		if(confirm){
			$.ajax({
				type: 'POST',
				url: '/delete_script',
				data: {script_name:script_name},
				success: function(){
					console.log(script_name+" deleted");
					$("#"+script_name).remove();
					location.reload();
				},
				error: function(request, status, error){
					failAlert(request.responseText);
				}
			});
		}
	},

	/**
	 * Save a script on the server
	 * @param {string} script_name the name of the script to save
	 * @param {string} script_data the data of the script to save
	 */
	saveScript: function(script_name, script_data){
		$.ajax({
			type: 'POST',
			url: '/save_script',
			data: {script_name:script_name, script_data:script_data},
			success: function(){
				console.log(script_name+" saved");
				location.reload();
			},
			error: function(request, status, error){
				failAlert(request.responseText);
			}
		});
	}

}
