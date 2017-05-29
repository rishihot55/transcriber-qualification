"""Data Upload Routes."""
from app.routes import api
from app.helpers.decorators import admin, transcriber, voicer
from app.helpers.data import prompts, recordings, transcripts
from app.helpers.format import clean_transcript, is_audio_file
from app.helpers.forms import TranscriptForm

from flask import abort, jsonify, render_template, request, session


@api.route('/prompts/add', methods=['GET'])
@admin
def render_prompt_form():
    return render_template('upload/prompt.html')


@api.route('/prompts', methods=['GET'])
@voicer
def get_voicing_prompt():
    user = session['user']
    return jsonify(prompts.retrieve_random_unvoiced_prompt(user['user_number']))


@api.route('/prompts', methods=['POST'])
@admin
def add_prompt():
    prompt = request.form.get('prompt')
    prompts.add(prompt)
    return jsonify({'prompt': prompt})


@api.route('/transcripts', methods=['GET'])
@transcriber
def render_transcript_submit_form():
    return render_template('upload/transcript.html')


@api.route('/transcripts', methods=['POST'])
@transcriber
def submit_transcription():
    user = session['user']
    form = TranscriptForm(request.form)

    if not form.validate():
        abort(400)
    recording_id = form.recording_id.data
    transcript = form.transcript.data
    processed_transcript = clean_transcript(transcript)

    if recording_id in transcripts.transcribed_by_user(user['user_number']):
        abort(403)
    return jsonify({"transcript": transcript})


@api.route('/recordings/upload', methods=['GET'])
@voicer
def render_upload_recording():
    return render_template('upload/recording.html')


@api.route('/recordings', methods=['GET'])
@transcriber
def get_random_recording():
    user = session['user']
    return jsonify({"recording_id": recordings.retrieve_random_untranscribed_recording(user['user_number'])})


@api.route('/recordings/<recording_id>', methods=['GET'])
@transcriber
def download_recording(recording_id):
    return recordings.download_recording(recording_id)


@api.route('/recordings', methods=['POST'])
@voicer
def upload_file():
    prompt_id = request.form.get('prompt_id')
    if 'recording' not in request.files or not prompts.find_by_id(prompt_id):
        abort(400)
    file = request.files['recording']
    print(prompt_id)
    if not is_audio_file(file):
        abort(400)
    user = session['user']

    if 'p' + prompt_id in recordings.recordings_by_user(user['user_number']):
        abort(403)
    recording = recordings.add(user['user_number'], prompt_id, file)

    return jsonify({'recording': recording})
