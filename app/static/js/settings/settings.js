$(document).ready(function() {

  $("#addRelay").on("click", function(){
    var label=$("#newLabel").val();
    var pin=$("#newPin").val();
    var parity=$("#newParity").val();
    if (/\s/.test(label)) {
      alert("Un label de relai ne doit pas contenir d'espace.");
    }
    if (/\s/.test(parity)) {
      alert("Une parité ne doit pas contenir d'espace.");
    }
    else{
      $.post( "/save_relay", {rel_label:label, rel_pin:pin, rel_parity:parity}, function(){
        console.log(label+" saved");
        location.reload();
      });
      //location.reload();
    }
  });

  //checkbox permettant d'activer ou désactiver un relai
  $('input[name=enableRel]').on("change", function() {
    var rel_label=this.id.substr(this.id.indexOf('_')+1)
    enableRelay(rel_label)
  });

  //bouton permettant de supprimer le relai
  $('input[name=deleteRel]').on("click", function() {
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
  $.post( "/enable_relay", {rel_label:rel_label}, function(){
    console.log(rel_label+" updated");
  });
}

function deleteRelay(rel_label){
  var confirm = window.confirm("Etes vous sûr de vouloir supprimer le relai \'"+rel_label+"\' ?");
  if(confirm){
    $.post( "/delete_relay", {rel_label:rel_label}, function(){
      console.log(rel_label+" deleted");
      $("#"+rel_label).remove();
    });
  }
}
