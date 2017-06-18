var scope = {
	users: null
};

var PromptTableWidget = {
	settings: {
		promptsBody: $('#prompts > tbody')
	},

	init: function() {
		PromptService.all()
		.then(function(users) {
			scope.users = users
			PromptTableWidget.renderPrompts(users);
		});
	},

	bindUIActions: function() {

	},

	renderPrompts: function(prompts) {
		var data = []
		for (promptId in prompts) {
			data.push({
				"id": promptId,
				"text": prompts[promptId]
			});
		}
		populateTable(PromptTableWidget.settings.promptsBody, data, ["id", "text"]);
	}
};

var TranscriptTableWidget = {
	settings: {
		transcriptsBody: $('#transcripts > tbody')
	},

	init: function() {
		TranscriptTableWidget.retrieveTranscripts()
		.then(TranscriptTableWidget.renderTranscripts);
	},
};

var RecordingTableWidget = {
    settings: {
    	recordingsBody: $('#recordings > tbody')
    },

    init: function() {
    	RecordingTableWidget.retrieveRecordings()
    	.then(RecordingTableWidget.renderRecordings);
    },

    retrieveRecordings: function() {
    	return $.get("/recordings/all");
    },

    renderRecordings: function(recordings) {
    	var recordingsData = transformArrayObjectProperty(recordings, "file", RecordingTableWidget.bindFileToButton);
    	if (scope.users != null) {
    		recordingsData = transformArrayObjectProperty(recordingsData, "prompt_id", function(promptId) {
    			return scope.users[promptId];
    		});
    	}
    	populateTable(RecordingTableWidget.settings.recordingsBody, recordingsData, ["user_id", "prompt_id", "file"]);
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
		return $.ajax({
			method: "GET",
			url: "/recordings/" + audioFile
		});
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
	PromptTableWidget.init();
	RecordingTableWidget.init();
	RecordingManager.init();
})();