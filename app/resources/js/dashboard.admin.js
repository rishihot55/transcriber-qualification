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
		for (promptId in prompts) {
			var rowElement = document.createElement("TR");
			var rowText = '<td>' + idx + '</td><td>' + promptId + '</td><td>' + prompts[promptId] + '</td>';
			rowElement.innerHTML = rowText ;
			PromptTableWidget.settings.promptsBody.append(rowElement);
			promptId += 1;
		}
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