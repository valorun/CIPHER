$(document).ready(function() {

  $("#addRelay").on("click", function(){
    var label=$("#newLabel").val();
    var pin=$("#newPin").val();
    $.post( "/save_relay", {rel_label:label, rel_pin:pin}, function(){
      console.log(label+" saved");
    });
    location.reload(); 
  });

  $('input[name=enableRel]').on("change", function() {
    var rel_label=this.id.substr(this.id.indexOf('_')+1)
    enableRelay(rel_label)
  });

  $('input[name=deleteRel]').on("click", function() {
    var rel_label=this.id.substr(this.id.indexOf('_')+1)
    deleteRelay(rel_label)
  });

});

//enable OR disable relay
function enableRelay(rel_label){
  $.post( "/enable_relay", {rel_label:rel_label}, function(){
    console.log(rel_label+" updated");
  });
}

function deleteRelay(rel_label){
  var confirm = window.confirm("Etes vous sûr de voulir supprimer le relai \'"+rel_label+"\' ?");
  if(confirm){
    $.post( "/delete_relay", {rel_label:rel_label}, function(){
      console.log(rel_label+" deleted");
      $("#"+rel_label).remove();
    });
  }
}