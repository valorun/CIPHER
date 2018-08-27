var trainingController = {
	init: function(){
		this.bind();
	},
	bind: function(){
		//button to add the sentence to the conversation
  		$("#addToConvButton").on("click", () => {
  			var sentence=$( "#currentSentence" ).val();
  			if(sentence===null || sentence===""){
				failAlert("La phrase fournie est vide.");
  				return;
  			}
  			var response="";
  			var sequence=$( "#currentSequence" ).val();
  			if(sequence!==null && sequence!==""){
  				response="["+sequence+"]";
  			}
  			response+=$("#currentResponse" ).val()
  			if(response===null || response===""){
				failAlert("La réponse fournie et vide.");
  				return;
  			}
  			this.addToConversation(sentence, response);
  		});

  		$( "#conversation" ).sortable();
  		$( "#conversation" ).disableSelection();

  		//button that trigger the training
  		$("#trainButton").on("click", () => {
  			this.train();
  		});
	},
	train: function(){
		var conversation=[];

  		$("#conversation").children().each(function (i) {
  			conversation.push($(this).find(".sentence").text());
  			conversation.push($(this).find(".response").text());
  		});
  		$("#conversation").empty();
  		socket.emit('train', conversation);
	},
	addToConversation: function(sentence, response){
		var convItem="<li class='container round-large light-grey border display-container'>"+
  						"<span class='display-left xlarge'><i class='fas fa-sort'></i></span>"+
  						"<div class='margin-left' style='word-wrap: break-word'>" +
							"<p class='large sentence'>"+sentence+"</p>"+
  							"<p class='response'>"+response+"</p>"+
						"</div>"+
  						"<span class='display-right button xlarge deleteConvItem'><i class='fas fa-trash'></i></span>"+
					"</li>";

  		$( "#conversation" ).append(convItem);

   	 	//button to delete the sentence
   	 	$(".deleteConvItem").on("click", function(){
   	 		$(this).parent().remove();
   	 	});
	}
}
