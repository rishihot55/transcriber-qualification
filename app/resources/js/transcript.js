var s,
TranscriptManager = {
	settings: {
		audioElement: $('#audio')[0],
		sourceElement: $('#source'),
		recordingField: $('#recording-id')
	},

	bindUIElements: function() {

	},

	init: function() {
		s = this.settings;
		TranscriptManager.retrieveRecording()
		.then(TranscriptManager.prepareAudio);
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
	}
};

(function() {
	TranscriptManager.init();
})();