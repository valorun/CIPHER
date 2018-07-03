var speechRec = new JsSpeechRecognizer();
speechRec.openMic();
var treshold=0.5; //seuil minimun de reconnaissance

$(document).ready(function() {

    socket.on('load_keywords_dataset', function(dataset) {
        speechRec.model=dataset[0];
        speechRec.wordBuffer=dataset[1];
        speechRec.modelBuffer=dataset[2];
        console.log(speechRec.model);
        console.log(speechRec.wordBuffer);
        console.log(speechRec.modelBuffer);
    });

    //bouton d'entrainement
    $("#startStopRecordingButton").click(function() {
        if (!speechRec.isRecording()) {
            var word = $("#currentKeyword").val();
            speechRec.startTrainingRecording(word);

            //actualise l'interface
            $("#startStopRecordingButton").val("Arrêter l'entrainement");
            $("#startStopRecognition").prop('disabled', true);

        } else {
            var recordingId = speechRec.stopRecording();

            //actualise l'interface
            $("#startStopRecordingButton").val("Lancer l'entrainement");
            $("#startStopRecognition").prop('disabled', false);

            //ajoute le nouvel échantillon à la liste
            var playbackDivId = "playbackResultId" + recordingId;
            var playButtonId = "playRecordingButton" + recordingId;
            var deleteButtonId = "deleteRecordingButton" + recordingId;
            
            var appendHtml = '<tr id=' + playbackDivId + '>';
            appendHtml += '<td>enregistrement #' + recordingId +' pour le mot <b>' + $("#currentKeyword").val() + '</b></td>';
            appendHtml += '<td><input type="button" class="button blue" value="lire" id="' + playButtonId + '" /></td>';
            appendHtml += '<td><input type="button" class="button blue" value="supprimer" id="' + deleteButtonId + '" /></td>';
            appendHtml += '</tr>';

            $("#training").append(appendHtml);

            //ajoute le bouton de lecture
            var finalPlaybackId = recordingId - 1;
            $("#" + playButtonId).click(function() {
                speechRec.playTrainingBuffer(finalPlaybackId);
            });

            //ajoute le bouton de suppression
            $("#" + deleteButtonId).click(function() {
                $("#" + playbackDivId).hide();
                speechRec.deleteTrainingBuffer(finalPlaybackId);
                speechRec.generateModel();
            });

            //recharge le modèle
            speechRec.generateModel();

        }
    });
    
    //bouton permettant de sauvegarder le modèle
    $("#saveButton").click(function() {
        var json=[];
        json.push(speechRec.model);
        json.push(speechRec.wordBuffer);
        json.push(speechRec.modelBuffer);
        socket.emit('save_keywords_dataset', JSON.stringify(json));
    });

    //bouton permettant de lancer la reconnaissance
    $("#startStopRecognition").click(function() {
        if (!speechRec.isRecording() && !recognizing) {
            // Update the UI and prevent the training button from being pressed
            $("#startStopRecognition").val("Arrêter la reconnaissance");
            $("#startStopRecordingButton").prop('disabled', true);

            speechRec.startKeywordSpottingRecording();
        } else {
            $("#startStopRecognition").val("Lancer la reconnaissance");
            $("#startStopRecordingButton").prop('disabled', false);

            speechRec.stopRecording();
        }
        speechRec.keywordSpottingMinConfidence = treshold;
    });

    //fonction appelée quand le mot clé est reconnu
    var updateKeywordSpotting = function(result) {
        if(!recognizing){
            var timeId = new Date().getTime();
            var playbackDivId = "playbackKeywordSpotId" + timeId;

            var appendHtml = '<li id=' + playbackDivId + '>';
            appendHtml += '<b> '+ result.match + '</b> ';
            appendHtml += '</li>';

            $("#detectionResult").append(appendHtml);
            startDictation(); //on commence la reconnaissance quand le mot est reconnu
        }
    };
    speechRec.keywordSpottedCallback=updateKeywordSpotting;

    //on charge le modèle déjà enregistrés
    socket.emit('load_keywords_dataset');

});