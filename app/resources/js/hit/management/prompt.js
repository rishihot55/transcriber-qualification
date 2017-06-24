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

var HitPromptConversionManager = {
	settings: {
		combobox: $('#prompt-combobox'),
		convertButton: $('#convert-prompt-button')
	},

	bindUIActions: function() {
		var s = HitPromptConversionManager.settings;

		s.convertButton.click(function() {
			if (s.combobox.val() !== "") {
				HitPromptConversionManager.convertPrompt(s.combobox.val())
				.then(function() {
					StatusWidget.showSuccess("The prompt has been converted successfully to a HIT prompt!");
					HitPromptService.unconverted()
					.then(HitPromptConversionManager.prepareCombobox);
				})
			}
		});
	},

	init: function() {
		HitPromptConversionManager.bindUIActions();
		HitPromptService.unconverted()
		.then(HitPromptConversionManager.prepareCombobox);
	},

	prepareCombobox: function(prompts) {
		var s = HitPromptConversionManager.settings;

		var fragment = document.createDocumentFragment();
		for (promptId in prompts) {
			var optionElement = document.createElement("option");
			optionElement.text = prompts[promptId];
			optionElement.value = promptId;
			fragment.appendChild(optionElement);
		}

		s.combobox.append(fragment);
		s.combobox.combobox();
	},

	convertPrompt: function(promptId) {
		return $.ajax({
			method: "POST",
			url: "/hit/prompts/convert",
			data: {
				"prompt_id": promptId
			}
		});
	}
};

(function() {
	HitPromptTableWidget.init();
	HitPromptConversionManager.init();
})();