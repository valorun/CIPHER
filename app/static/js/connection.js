var socket;
var voices

$(document).ready(function() {
  socket = io.connect(window.location.host+'/client');
  socket.on('command', function(msg) {
    console.log('Message from server: ', msg);
  });

  window.speechSynthesis.onvoiceschanged = function() {
    voices=window.speechSynthesis.getVoices();
  }

	//reponse du serveur lors d'une de l'écoute d'une phrase
  socket.on('response', function(msg) {
    console.log('Message from server:', msg);
    if ('speechSynthesis' in window) {
      var to_speak = new SpeechSynthesisUtterance(msg);

      $.each(voices,function(){
        if(Cookies.get("voice") === this.name){
          to_speak.voice= this;
        }
      });
      window.speechSynthesis.speak(to_speak);
   }
 });

  socket.on('play_sound', function(sound_name) {
    var audio = new Audio(window.location.origin+'/play_sound/'+sound_name);
    audio.play();
  });

});
