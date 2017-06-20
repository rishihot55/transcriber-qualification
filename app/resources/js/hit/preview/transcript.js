// No need to write any actual logic. Functionality is fully stubbed out.
var TranscriptPreviewManager = {
	settings: {
		audioElement: $('#audio')[0],
		sourceElement: $('#source'),
		submitButton: $("#submit-button"),
		transcriptField: $("#transcript"),
		form: $('#preview-form'),
		recordingList: [
			"http://packs.shtooka.net/eng-balm-judith-proverbs/mp3/eng-8f775a01.mp3",
			"http://packs.shtooka.net/eng-balm-judith-proverbs/mp3/eng-3c82e1de.mp3",
			"http://packs.shtooka.net/eng-wims-mary-conversation/mp3/eng-8cddd713.mp3"],
	},

	init: function() {
		console.log("Init called");
		TranscriptPreviewManager.bindUIActions();
		TranscriptPreviewManager.loadRecording();
	},

	bindUIActions: function() {
		var s = TranscriptPreviewManager.settings;
		s.submitButton.click(function(e) {
			if (!TranscriptPreviewManager.validateTranscript(s.transcriptField.val())) {
				StatusWidget.showError('Please enter a valid transcription');
				return;
			}
			s.transcriptField.val("");
			StatusWidget.showSuccess('The transcript has been submitted successfully');
			TranscriptPreviewManager.loadRecording();
		});
		
	},

	validateTranscript: function(transcript) {
		return Validator.validate([
			[transcript, [Validator.rules.regexp(/^[\w.,?"';: ]+$/)]]
		]);
	},

	prepareAudio: function(url) {
		var s = TranscriptPreviewManager.settings;
		s.sourceElement.attr('src', url);
		s.audioElement.load();
	},

	loadRecording: function() {
		var s = TranscriptPreviewManager.settings;
		var list = s.recordingList;
		if (list.length == 0) {
			s.form.hide();
			StatusWidget.showSuccess('There are no more recordings left to transcribe. You will be notified about the reward soon. Thank you!');
			return;
		}
		var url = list.shift();
		console.log("Loading recording ", url);
		TranscriptPreviewManager.prepareAudio(url);
	}
};

(function() {
	console.log("Loaded");
	TranscriptPreviewManager.init();
})();