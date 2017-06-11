PromptTableWidget = {
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

		console.log(data);

		populateTable(PromptTableWidget.settings.promptsBody, data, ["id", "text"]);
	}
};

TranscriptTableWidget = {
	settings: {
		transcriptsBody: $('#transcripts > body')
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

(function() {
	PromptTableWidget.init();
})();