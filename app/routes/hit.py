from app.routes import api
from app.helpers.decorators import admin
from app.helpers.stores import users, hit_prompts, hit_recordings
from app.helpers.format import parse_recording_data

from flask import abort, render_template, request, session, jsonify


@api.route('/hit/manage', methods=['GET'])
@admin
def render_manage_hit():
    return render_template('hit/management.html')


@api.route('/hit/prompts/all', methods=['GET'])
def get_all_hit_prompts():
    return jsonify(hit_prompts.all())


@api.route('/hit/prompts', methods=['POST'])
@admin
def create_prompt_external_question():
    pass


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
