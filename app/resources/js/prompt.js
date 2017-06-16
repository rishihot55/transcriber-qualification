var s,
PromptManager = {
	settings: {
		form: $('form'),
		promptField: $('#prompt') 
	},

	init: function() {
		s = this.settings;
		this.bindUIActions();
	},

	bindUIActions: function() {
		s.form.submit(function(e) {
			e.preventDefault();

			if (!PromptManager.validatePrompt(s.promptField.val())) {
				StatusWidget.showError('Please enter a valid prompt');
				return;
			}

			PromptService.create(s.promptField.val())
			.then(function() {
				StatusWidget.showSuccess('Prompt has been added successfully');
				PromptManager.clearFields();
			})
			.catch(handleError);
		})
	},

	validatePrompt: function(prompt) {
		return Validator.validate([
			[prompt, [Validator.rules.regexp(/^[\w.,?"';: ]+$/)]]
		]);
	},

	clearFields: function() {
		s.promptField.val('');
	}
};

(function() {
	PromptManager.init();
})();