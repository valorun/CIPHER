$(document).ready(function() {
  $('input[name=enableSeq]').on("change", function() {
    var seq_name=this.id.substr(this.id.indexOf('_')+1);
    enableSequence(seq_name)
  });
  $('input[name=deleteSeq]').on("click", function() {
    var seq_name=this.id.substr(this.id.indexOf('_')+1)
    deleteSequence(seq_name)
  });

});

//enable OR disable sequence
function enableSequence(seq_name){
  $.post( "/enable_sequence", {seq_name:seq_name}, function(){
    console.log(seq_name+" updated");
  });
}

function deleteSequence(seq_name){
  var confirm = window.confirm("Etes vous sûr de voulir supprimer la séquence \'"+seq_name+"\' ?");
  if(confirm){
    $.post( "/delete_sequence", {seq_name:seq_name}, function(){
      console.log(seq_name+" deleted");
      $("#"+seq_name).remove();
    });
  }
}
