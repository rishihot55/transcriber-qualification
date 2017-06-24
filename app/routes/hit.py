from app.routes import api
from app.helpers.decorators import admin
from app.helpers.stores import users, prompts, hit_prompts, hit_recordings
from app.helpers.format import parse_recording_data

from flask import abort, render_template, request, session, jsonify


@api.route('/hit/manage', methods=['GET'])
@admin
def render_manage_hit():
    return render_template('hit/management.html')


@api.route('/hit/prompts', methods=['GET'])
@admin
def render_manage_hit_prompts():
    return render_template('hit/management/prompt.html')


@api.route('/hit/prompts/all', methods=['GET'])
@admin
def get_all_hit_prompts():
    return jsonify(hit_prompts.all())


@api.route('/hit/prompts', methods=['POST'])
@admin
def create_hit_prompt():
    prompt = request.form.get('prompt')
    if not prompt:
        abort(400)
    if prompt in hit_prompts.all().values():
        abort(403)
    hit_prompts.add(prompt)
    return jsonify({'prompt': prompt})


@api.route('/hit/prompts/unconverted', methods=['GET'])
@admin
def get_unconverted_prompts():
    converted_prompt_texts = hit_prompts.all().values()
    prompt_list = prompts.all()
    unconverted_prompts = {
        prompt_id: text for (prompt_id, text) in prompt_list.items()
        if text not in converted_prompt_texts}
    return jsonify(unconverted_prompts)


@api.route("/hit/prompts/convert", methods=['POST'])
@admin
def convert_existing_prompt_to_hit():
    if 'prompt_id' not in request.form:
        abort(400)

    prompt_id = request.form['prompt_id']
    prompt = prompts.find_by_id(prompt_id)
    if not prompt:
        abort(400)
    converted_prompt_texts = hit_prompts.all().values()
    prompt_list = prompts.all()
    unconverted_prompts = {
        prompt_id: text for (prompt_id, text) in prompt_list.items()
        if text not in converted_prompt_texts}
    if prompt_id not in unconverted_prompts:
        abort(403)

    new_prompt = hit_prompts.add(prompt)

    return jsonify(new_prompt)

@api.route('/hit/recordings', methods=['GET'])
def render_manage_hit_recordings():
    return render_template('hit/management/recording.html')

@api.route('/hit/recordings/all', methods=['GET'])
@admin
def get_all_hit_recordings():
    recording_data = [
        parse_recording_data(recording)
        for recording in hit_recordings.all()]
    return jsonify(recording_data)


@api.route('/hit/recordings/<recording_id>', methods=['GET'])
def download_hit_recording(recording_id):
    return hit_recordings.download_recording(recording_id)


@api.route('/hit/recordings', methods=['POST'])
@admin
def create_recording_external_question():
    pass


@api.route("/hit/recordings/convert", methods=['POST'])
@admin
def convert_existing_recording_to_hit():
    pass


@api.route('/hit/transcript', methods=['GET'])
def render_transcription_hit():
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


@api.route('/hit/recording', methods=['GET'])
def render_recording_hit():
    group = request.args.get('group')

    if not group:
        abort(400)

    worker_id = request.args.get('workerId')
    assignment_id = request.args.get('assignmentId')
    submit_url = request.args.get('turkSubmitTo')

    if not worker_id or not assignment_id or not submit_url:
        abort(400)
    if worker_id == "ASSIGNMENT_ID_NOT_AVAILABLE":
        return render_template("hit/preview/recording.html")

    user = users.find_by_id(worker_id)
    if not user:
        user = users.add(
            worker_id, '001', 'turker', 'assignment {}'.format(assignment_id))
    session['user'] = user

    return render_template('hit/recording.html')
