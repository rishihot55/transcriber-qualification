var RecordingPreviewManager = {
	settings: {
		promptList: [
			"We drank tea in the afternoon and watched TV",
			"Are you a leader or a follower?",
			"A bad workman always blames his tools"],
		promptText: $('#prompt-text'),
		uploadButton: $('#upload'),
		recording: $('#recording'),
		file: null,
		panel: $('#panel')
	},

	init: function() {
		RecordingPreviewManager.loadPrompt();
		RecordingPreviewManager.bindUIActions();
	},

	bindUIActions: function() {
		var s = this.settings;
		s.recording.on('change', RecordingPreviewManager.prepareFile);
		s.uploadButton.click(function(e) {
			if (!RecordingPreviewManager.validateRecording(s.file)) {
				StatusWidget.showError("Please upload a valid recording");
				return;
			}

			StatusWidget.showSuccess("The recording has been uploaded successfully. A new prompt has been loaded");
			s.file = null;
			s.recording.val('');
			RecordingPreviewManager.loadPrompt();
		});
	},

	loadPrompt: function() {
		var s = this.settings;
		var list = s.promptList;

		if (list.length == 0) {
			s.panel.hide();
			StatusWidget.showSuccess("There are no more prompts left to record. You will be notified about your reward. Thank You!");
			return;
		}

		var prompt = list.shift();
		s.promptText.text(prompt);
	},

	prepareFile: function(e) {
		RecordingPreviewManager.settings.file = e.target.files[0];
	},

	validateRecording: function(recording) {
		return Validator.validate([
			[recording, [Validator.rules.audioFile]]
		]);
	},
};

(function() {
	RecordingPreviewManager.init();
})();