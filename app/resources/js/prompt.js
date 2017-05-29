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

			PromptManager.sendPrompt(s.promptField.val())
			.then(function() {
				StatusWidget.showSuccess('Prompt has been added successfully');
				PromptManager.clearFields();
			})
			.catch(handleError);
		})
	},

	validatePrompt: function(prompt) {
		return Validator.validate([
			[prompt, [Validator.rules.required, Validator.rules.regexp(/^[\w.,?"':]+$/)]]
		]);
	},

	sendPrompt: function(prompt) {
		return $.ajax({
			method: 'POST',
			url: '/prompts',
			data: {
				'prompt': prompt
			}
		});
	},

	clearFields: function() {
		s.promptField.val('');
	}
};

(function() {
	PromptManager.init();
})();