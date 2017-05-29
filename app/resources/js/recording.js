var s,
RecordingManager = {
	settings: {
		promptIdField: $('#prompt-id'),
		promptField: $('#prompt-text'),
		recording: $('#recording'),
		form: $('form'),
		file: null
	},

	bindUIElements: function() {
		s.recording.on('change', RecordingManager.prepareFile);
		s.form.submit(function(e) {
			e.preventDefault();
			if (!RecordingManager.validateRecording(s.file)) {
				StatusWidget.showError('Please upload a valid recoding');
				return;
			}

			RecordingManager.uploadRecording(
				s.promptIdField.val(),
				s.file)
			.then(function() {
				StatusWidget.showSuccess('The file has been uploaded successfully');
				RecordingManager.clearFields();
				RecordingManager.loadPrompt();
			});
		});
	},

	init: function() {
		s = this.settings;
		RecordingManager.loadPrompt();
		RecordingManager.bindUIElements();
	},

	loadPrompt: function() {
		RecordingManager.retrievePrompt()
		.then(RecordingManager.setPrompt);
	},

	retrievePrompt: function() {
		return $.ajax({
			method: 'GET',
			url: '/prompts'
		});
	},

	setPrompt: function(data) {
		s.promptIdField.val(data.prompt_id);
		s.promptField.text(data.text);
	},

	uploadRecording: function(promptId, recording) {
		var formData = new FormData();

		formData.append('prompt_id', promptId);
		formData.append('recording', recording);

		return $.ajax({
			url: '/recordings',
			method: 'POST',
			data: formData,
			cache: false,
			dataType: 'json',
			processData: false,
			contentType: false,
		});
	},

	prepareFile: function(e) {
		s.file = e.target.files[0];
	},

	validateRecording: function(recording) {
		return Validator.validate([
			[recording, [Validator.rules.audioFile]]
		]);
	},

	clearFields: function() {
		s.promptIdField.val('');
		s.file = null;
		s.recording.val('');
		s.promptField.text('');
	}
};

(function() {
	RecordingManager.init();
})();