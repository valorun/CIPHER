var speechDetectionController = {
    dictationController: dictationController,
    trainingController: trainingController,

    speechRec: null,
    treshold: 0.5,

    init: function(){
        this.dictationController.init();
        this.trainingController.init();

        this.speechRec = new JsSpeechRecognizer();
        this.speechRec.openMic();
        this.speechRec.keywordSpottedCallback = this.updateKeywordSpotting;
		this.speechRec.keywordSpottingMinConfidence = this.treshold;
        this.bind();

        //load the generated model
        socket.emit('load_keywords_dataset');
    },
    bind: function(){
        socket.on('load_keywords_dataset', (dataset) => {
            this.loadModel(dataset);
        });

        //button to save the model
        $("#saveButton").click(() => {
            this.saveModel();
        });

        $("#startStopRecordingButton").click(() => {
            this.startStopRecordingButton();
        });

        //button to start recognition
        $("#startRecognition").click(() => {
            if (!this.speechRec.isRecording() && !this.dictationController.recognizing) {
                // update the UI and prevent the training button from being pressed
                $("#startStopRecordingButton").prop('disabled', true);
                this.speechRec.startKeywordSpottingRecording();
				$("#speechDetectionModal").show();
            } else {
                $("#startStopRecordingButton").prop('disabled', false);
                this.speechRec.stopRecording();
            }
        });

		$("#stopRecognition").click(() => {
			$("#startStopRecognition").val("Lancer la reconnaissance");
			$("#startStopRecordingButton").prop('disabled', false);

			this.speechRec.stopRecording();
			$("#speechDetectionModal").hide();
		});

    },
    loadModel: function(dataset){
        if(dataset.length > 0){
            this.speechRec.model=dataset[0];
            this.speechRec.wordBuffer=dataset[1];
            this.speechRec.modelBuffer=dataset[2];
        }
        console.log(this.speechRec.model);
        console.log(this.speechRec.wordBuffer);
        console.log(this.speechRec.modelBuffer);
    },
    saveModel: function(){
        var json=[];
        json.push(this.speechRec.model);
        json.push(this.speechRec.wordBuffer);
        json.push(this.speechRec.modelBuffer);
        socket.emit('save_keywords_dataset', JSON.stringify(json));
		successAlert("Le modèle a été enregistré");
    },
    startStopRecordingButton: function(){
        if (!this.speechRec.isRecording()) {
            var word = $("#currentKeyword").val();
            this.speechRec.startTrainingRecording(word);

            //refresh UI
            $("#startStopRecordingButton").val("Arrêter l'entrainement");
            $("#startStopRecognition").prop('disabled', true);

        } else {
            var recordingId = this.speechRec.stopRecording();

            //refresh UI
            $("#startStopRecordingButton").val("Lancer l'entrainement");
            $("#startStopRecognition").prop('disabled', false);

            //add the new samble to the list
            var playbackDivId = "playbackResultId" + recordingId;
            var playButtonId = "playRecordingButton" + recordingId;
            var deleteButtonId = "deleteRecordingButton" + recordingId;

            var appendHtml = '<tr id=' + playbackDivId + '>';
            appendHtml += '<td>enregistrement #' + recordingId +' pour le mot <b>' + $("#currentKeyword").val() + '</b></td>';
            appendHtml += '<td><a type="button" class="button secondary" value="lire" id="' + playButtonId + '" ><i class="fas fa-play"></i></a></td>';
            appendHtml += '<td><a type="button" class="button secondary" id="' + deleteButtonId + '" ><i class="fas fa-trash"></i></a></td>';
            appendHtml += '</tr>';

            $("#training").append(appendHtml);

            //add a button to play the training
            var finalPlaybackId = recordingId - 1;
            $("#" + playButtonId).click(() => {
                this.speechRec.playTrainingBuffer(finalPlaybackId);
            });

            //add a button to delete training
            $("#" + deleteButtonId).click(() => {
                $("#" + playbackDivId).hide();
                this.speechRec.deleteTrainingBuffer(finalPlaybackId);
                this.speechRec.generateModel();
            });

            //reload the model
            this.speechRec.generateModel();
        }
    },

    /**
     * function called when a keyword is recognized
     */
    updateKeywordSpotting: (result) => {
        if(!this.dictationController.recognizing){
            let timeId = new Date().getTime();
            let keywordSpottedId = "keywordSpotted" + timeId;

            let appendHtml = "<li id='" + keywordSpottedId + "'>" +
            					"<strong>" + result.match + "</strong>" +
            				"</li>";

            $("#detectionResult").append(appendHtml);
			$("#detectionResult").parent().scrollTop($("#detectionResult").parent().height());
            this.dictationController.startDictation(); //start the dictation when the keyword is detected
        }
    }
}
