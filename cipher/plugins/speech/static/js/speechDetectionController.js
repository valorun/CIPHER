var speechDetectionController = {
    recognizing: false,

    init: function(){
        this.bind();
    },
    bind: function(){

        $("#startStopRecordingButton").click(() => {
            this.startStopRecordingButton();
        });

        //button to start recognition
        $("#startRecognition").click(() => {
            if (!$("#startStopRecordingButton").prop('disabled')) {
                // update the UI and prevent the training button from being pressed
                $("#startStopRecordingButton").prop('disabled', true);
				$("#speechDetectionModal").show();
            } else {
                $("#startStopRecordingButton").prop('disabled', false);
            }
        });

		$("#stopRecognition").click(() => {
			$("#startStopRecognition").val("Lancer la reconnaissance");
			$("#startStopRecordingButton").prop('disabled', false);

			$("#speechDetectionModal").hide();
        });
        
        //server response when a sentence must be play on the client
		socket.on('response', (msg) => {
			let time = new Date();
			$("#detectionResult").append("<li>"+
											"<div class='row'>"+
												"<div class='col l2 m2 s3 center'>" +
													"<span class='border circle large btn hover-none'><i class='fas fa-robot fa-fw'></i></span>" +
												"</div>" +
												"<div class='container round-large light-grey border col l10 m10 s9'>" +
													"<div class='left-align'><p>" +
														msg +
													"</p></div>"+
													"<div class='right-align'><p>" + time.getHours() + ":" + time.getMinutes() + "</p></div>" +
												"</div>" +
											"</div>" +
										"</li>");
			$("#detectionResult").parent().scrollTop($("#detectionResult").parent().height());
		});

    },
}
