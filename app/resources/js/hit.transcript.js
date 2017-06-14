var s,
HitTranscriptManager = {
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
			if (!HitTranscriptManager.validateTranscript(s.transcriptField.val())) {
				StatusWidget.showError('Please enter a valid transcription');
				return;
			}

			HitTranscriptManager.sendTranscript(
				s.transcriptField.val(),
				s.recordingField.val()
				).then(function() {
					StatusWidget.showSuccess('The transcript has been submitted successfully');
					HitTranscriptManager.loadRecording();
				});
		})
	},

	init: function() {
		s = this.settings;
		HitTranscriptManager.bindUIElements();
		HitTranscriptManager.loadRecording();
	},

	loadRecording: function () {
		HitTranscriptManager.retrieveRecording()
		.then(function(data) {
			if (data.recording_id === -1) {
				StatusWidget.showError('There are no more recordings left to transcribe. Please check again later!');
				s.transcriptForm.hide();
				return;
			}

			HitTranscriptManager.prepareAudio(data);
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

	turkSubmit: function(transcript, recordingId) {
	    return $.ajax({
	        method: "POST",
	        url: ""
	    })
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
	HitTranscriptManager.init();
})();