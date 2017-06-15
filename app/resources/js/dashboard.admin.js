var PromptTableWidget = {
	settings: {
		promptsBody: $('#prompts > tbody')
	},

	init: function() {
		PromptTableWidget.retrievePrompts()
		.then(PromptTableWidget.renderPrompts)
	},

	bindUIActions: function() {

	},

	retrievePrompts: function() {
		return $.ajax({
			method: "GET",
			url: "/prompts/all",
		});
	},

	renderPrompts: function(prompts) {
		var idx = 1;
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

	retrieveTranscripts: function() {
		
	},

	renderTranscripts: function() {

	}

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
    	populateTable(RecordingTableWidget.settings.recordingsBody, recordings, ["user_id", "prompt_id"]);
    }
};

(function() {
	PromptTableWidget.init();
	RecordingTableWidget.init();
})();