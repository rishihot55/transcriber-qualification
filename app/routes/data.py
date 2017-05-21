"""Data Upload Routes."""
from app.routes import api
from app.helpers.decorators import admin, transcriber, voicer
from app.helpers.data import prompts

from flask import jsonify, render_template, request


@api.route('/prompt', methods=['GET'])
@admin
def render_prompt_form():
    return render_template('upload/prompt.html')


@api.route('/prompt', methods=['POST'])
@admin
def add_prompt():
    prompt = request.form.get('prompt')
    processed_prompt = process_prompt(prompt)
    prompts.add(prompt)
    return jsonify({'prompt': prompt})


@api.route('/transcript', methods=['GET'])
@transcriber
def render_transcript_submit_form():
    return render_template('upload/transcript.html')


@api.route('/recording', methods=['GET'])
@voicer
def render_upload_recording():
    return render_template('upload/recording.html')


@api.route('/recording/<recording_id>', methods=['GET'])
@transcriber
def retrieve_recording():
    pass


@api.route('/recording', methods=['POST'])
@voicer
def upload_file():
    pass