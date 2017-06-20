"""Data Upload Routes."""
from app.routes import api
from app.helpers.decorators import admin, transcriber, voicer, user
from app.helpers.stores import prompts, recordings, transcripts, users
from app.helpers.format import clean_transcript, is_audio_file, parse_recording_data
from app.helpers.forms import TranscriptForm

from flask import abort, jsonify, render_template, request, session


@api.route('/prompts/add', methods=['GET'])
@admin
def render_prompt_form():
    return render_template('upload/prompt.html')


@api.route('/prompts/all', methods=['GET'])
@admin
def get_all_prompts():
    return jsonify(prompts.all())


@api.route('/prompts', methods=['GET'])
@voicer
def get_voicing_prompt():
    user = session['user']
    return jsonify(
        prompts.retrieve_random_unvoiced_prompt(
            recordings, user['user_number']))


@api.route('/prompts', methods=['POST'])
@admin
def add_prompt():
    prompt = request.form.get('prompt')
    prompts.add(prompt)
    return jsonify({'prompt': prompt})


@api.route('/transcripts/all', methods=['GET'])
@admin
def get_all_transcripts():
    transcript_data = [
        parse_transcript_data(transcript) for transcript in transcripts.all()]
    return jsonify(transcript_data)

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
    dir(form)
    recording_id = request.form['recording_id']
    transcript = form.transcript.data
    processed_transcript = clean_transcript(transcript)
    if not recordings.exists(recording_id):
        abort(400)
    if recording_id in transcripts.transcribed_by_user(user['user_number']):
        abort(403)

    user = session['user']
    transcripts.add(user['user_number'], recording_id, processed_transcript)
    return jsonify({"transcript": transcript})


@api.route('/recordings/upload', methods=['GET'])
@voicer
def render_upload_recording():
    return render_template('upload/recording.html')

@api.route('/recordings/all', methods=['GET'])
@admin
def get_all_recordings():
    recording_data = [parse_recording_data(recording) for recording in recordings.all()]
    return jsonify(recording_data)

@api.route('/recordings', methods=['GET'])
@transcriber
def get_random_recording():
    user = session['user']
    return jsonify({"recording_id": recordings.retrieve_random_untranscribed_recording(user['user_number'])})


@api.route('/recordings/<recording_id>', methods=['GET'])
@user
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


@api.route('/hit/manage', methods=['GET'])
@admin
def render_manage_hit():
    return render_template('hit/management.html')


@api.route('/hit/prompt', methods=['POST'])
@admin
def create_prompt_external_question():
    pass


@api.route('/hit/recording', methods=['POST'])
@admin
def create_recording_external_question():
    pass

@api.route('/hit', methods=['GET'])
def render_external_question():
    group = request.args.get('group')

    if not group:
        abort(400)

    worker_id = request.args.get('workerId')
    assignment_id = request.args.get('assignmentId')
    submit_url = request.args.get('turkSubmitTo')

    if not worker_id or not assignment_id or not submit_url:
        abort(400)
    if worker_id == "ASSIGNMENT_ID_NOT_AVAILABLE":
        return render_template("hit/preview/transcript.html")

    user = users.find_by_id(worker_id)
    if not user:
        user = users.add(
            worker_id, '010', 'turker', 'assignment {}'.format(assignment_id))
    session['user'] = user

    return render_template('hit/transcript.html')