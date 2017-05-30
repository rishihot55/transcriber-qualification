var s,
TranscriptManager = {
	settings: {
		audioElement: $('#audio')[0],
		sourceElement: $('#source'),
		recordingField: $('#recording-id'),
		transcriptField: $('#transcript'),
		transcriptForm: $('form')
	},

	bindUIElements: function() {
		s.transcriptForm.submit(function(e) {
			e.preventDefault();
			if (!TranscriptManager.validateTranscript(s.transcriptField.val())) {
				StatusWidget.showError('Please enter a valid transcription');
				return;
			}

			TranscriptManager.sendTranscript(
				s.transcriptField.val(),
				s.recordingField.val()
				).then(function() {
					StatusWidget.showSuccess('The transcript has been submitted successfully');
					TranscriptManager.loadRecording();
				});
		})
	},

	init: function() {
		s = this.settings;
		TranscriptManager.bindUIElements();
		TranscriptManager.loadRecording();
	},

	loadRecording: function () {
		TranscriptManager.retrieveRecording()
		.then(function(data) {
			if (data.recording_id === -1) {
				StatusWidget.showError('There are no more recordings left to transcribe. Please check again later!');
				s.transcriptForm.hide();
				return;
			}

			TranscriptManager.prepareAudio(data);
		});

	},

	retrieveRecording: function() {
		return $.ajax({
			method: 'GET',
			url: '/recordings'
		});
	},

	prepareAudio: function(data) {
		s.recordingField.val(data.recording_id);
		console.log(data.recording_id);
		s.sourceElement.attr('src', '/recordings/' + data.recording_id);
		console.log(s.audioElement)
		s.audioElement.load();
	},

	sendTranscript: function(transcript, recordingId) {
		return $.ajax({
			method: "POST",
			url: "/transcripts",
			data: {
				"transcript": transcript,
				"recording_id": recordingId
			}
		});
	},

	validateTranscript: function(transcript) {
		return Validator.validate([
			[transcript, [Validator.rules.regexp(/^[\w.,?"';: ]+$/)]]
		]);
	}
};

(function() {
	TranscriptManager.init();
})();