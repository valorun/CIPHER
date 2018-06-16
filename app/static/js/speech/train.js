$(document).ready(function() {
  //bouton pour ajouter à la conversation
  $("#addToConvButton").on("click", function(){
    var sentence=$( "#currentSentence" ).val();
    if(sentence===null || sentence===""){
      return
    }
    var response="";
    var sequence=$( "#currentSequence" ).val();
    if(sequence!==null && sequence!==""){
      response="["+sequence+"]";
    }
    response+=$("#currentResponse" ).val()
    if(response===null || response===""){
      return
    }
    var convItem="<li class='blue-grey display-container'>"+
    "<span class='display-left'><i class='fas fa-sort'></i></span>"+
    "<div style='word-wrap: break-word'><span class='large sentence'>"+sentence+"</span> <br>"+
    "<span class='response'>"+response+"</span></div>"+
    "<span class='display-right button large deleteConvItem'><i class='fas fa-trash'></i></span></li>";

    $( "#conversation" ).append(convItem);

    //bouton pour supprimer la phrase
    $(".deleteConvItem").on("click", function(){
      $(this).parent().remove();
    });
  });

  $( "#conversation" ).sortable();
  $( "#conversation" ).disableSelection();

  //déclenchement de l'entrainement
  $("#trainButton").on("click", function(){
    var conversation=[];

    $("#conversation").children().each(function (i) {
        conversation.push($(this).find(".sentence").text());
        conversation.push($(this).find(".response").text());
    });
    $("#conversation").empty();
    socket.emit('train', conversation);
  });
});