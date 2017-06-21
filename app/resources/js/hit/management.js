var scope = {
	prompts: null
};

var HitPromptTableWidget = {
	settings: {
		promptsBody: $('#prompts > tbody')
	},

	init: function() {
		HitPromptService.all()
		.then(function(prompts) {
			scope.prompts = prompts;
			HitPromptTableWidget.renderPrompts(prompts);
		});
	},

	renderPrompts: function(prompts) {
		var data = [];
		for (promptId in prompts) {
			data.push({
				"id": promptId,
				"text": prompts[promptId]
			});
		}
		populateTable(HitPromptTableWidget.settings.promptsBody, data, ["text"]);
	}
};

(function() {
	HitPromptTableWidget.init();
})();