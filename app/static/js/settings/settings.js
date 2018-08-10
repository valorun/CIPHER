$(document).ready(function() {

  $("#addRelay").on("click", function(){
    var label=$("#newLabel").val();
    var pin=$("#newPin").val();
    var parity=$("#newParity").val();

    $.ajax({
      type: 'POST',
      url: '/save_relay',
      data: {rel_label:label, rel_pin:pin, rel_parity:parity},
      success: function(){
        location.reload();
      },
      error: function(request, status, error){
        alertModal(request.responseText);
      }
    });
    //location.reload();
  });

  //checkbox permettant d'activer ou désactiver un relai
  $('input[name=enableRel]').on("change", function() {
    var rel_label=this.id.substr(this.id.indexOf('_')+1)
    enableRelay(rel_label)
  });

  //bouton permettant de supprimer le relai
  $('a[name=deleteRel]').on("click", function() {
    var rel_label=this.id.substr(this.id.indexOf('_')+1)
    deleteRelay(rel_label)
  });

  window.speechSynthesis.onvoiceschanged = function() {
    var voices=window.speechSynthesis.getVoices();
    console.log(voices);
    $.each(voices,function(){
      if(typeof Cookies.get('voice') !== 'undefined' && 
        Cookies.get('voice') === this.name){ //si il s'agit s'une voix déjà choisis, on la sélectionne
        $("#voices").append($("<option selected='selected'/>").val(this.name).text(this.name));
      }else {
        $("#voices").append($("<option />").val(this.name).text(this.name));
      }
    });
  };

  $("#voices").on("change", function() {
    Cookies.set("voice", $("#voices").val());
  })

  
});

//enable OR disable relay
function enableRelay(rel_label){
  $.ajax({
      type: 'POST',
      url: '/enable_relay',
      data: {rel_label:rel_label},
      success: function(){
        console.log(rel_label+" updated");
      },
      error: function(request, status, error){
        alertModal(request.responseText);
      }
    });
}

function deleteRelay(rel_label){
  var confirm = window.confirm("Etes vous sûr de vouloir supprimer le relai \'"+rel_label+"\' ?");
  if(confirm){
      $.ajax({
      type: 'POST',
      url: '/delete_relay',
      data: {rel_label:rel_label},
      success: function(){
              console.log(rel_label+" deleted");
      $("#"+rel_label).remove();
      },
      error: function(request, status, error){
        alertModal(request.responseText);
      }
    });
  }
}
