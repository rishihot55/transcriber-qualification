var scope = {
	prompts: null
};

var HitRecordingTableWidget = {
    settings: {
    	recordingsBody: $('#recordings > tbody')
    },

    init: function() {
    	HitRecordingService.all()
    	.then(HitRecordingTableWidget.renderRecordings);
    },

    renderRecordings: function(recordings) {
    	var recordingsData = transformArrayObjectProperty(recordings, "file", HitRecordingTableWidget.bindFileToButton);
    	if (scope.prompts != null) {
    		recordingsData = transformArrayObjectProperty(recordingsData, "prompt_id", function(promptId) {
    			return scope.prompts[promptId];
    		});
    	}
    	populateTable(HitRecordingTableWidget.settings.recordingsBody, recordingsData, ["user_id", "prompt_id", "file"]);
    	RecordingManager.bindUIActions();
    },

    bindFileToButton: function(file) {
    	return "<button class='btn btn-small btn-primary listen' value='" + file + "'' type='button'>Listen</button>";
    }
};

var RecordingManager = {
	settings: {
		listenButton: $('.listen'),
		audioElement: $('#audio')[0],
		sourceElement: $('#source'),
		currentRecording: null
	},

	init: function() {

	},

	bindUIActions: function() {
		// Bind buttons to listen audio
		$(document).on('click', '.listen', function() {
    		// Get the corresponding data and play
			var audioFile = $(this).val();
			// Bind the audio file
			RecordingManager.bindAudio(audioFile);
			RecordingManager.settings.audioElement.play();
    	});
	},

	retrieveAudio: function(audioFile) {
		return $.get("/hit/recordings/" + audioFile);
	},

	bindAudio: function(audioFile) {
		if (RecordingManager.settings.currentRecording !== audioFile) {
			RecordingManager.settings.sourceElement.attr('src', '/recordings/' + audioFile);
			RecordingManager.settings.audioElement.load();
			RecordingManager.settings.currentRecording = audioFile;
		}
	}
};

(function() {
	HitRecordingTableWidget.init();
	RecordingManager.init();
})();