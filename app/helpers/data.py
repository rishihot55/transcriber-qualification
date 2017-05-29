"""Data Management Helpers."""
import os
from shutil import copy2
from app.helpers.format import get_next_number, is_prompt_file, user_dict, is_recording, transcript_of_recording, is_transcript_file, recorded_by_user
from random import choice

from flask import send_file


class UserStore():
    """User Storage and Management."""

    def __init__(self):
        """
        Load the data from the flat file.

        TODO:
        - Add method
        - Update method
        """
        self.user_id_index = {}
        self.user_number_index = {}
        users_file_path = os.path.join('app', 'db', 'users.txt')
        with open(users_file_path, 'r') as users_file:
            for line in users_file:
                values = line.strip().split(":")
                (user_id, user_number, shash, rights, name, email) = values
                user = user_dict(
                    user_id, user_number, shash, rights, name, email
                )
                self.user_id_index[user_id] = user
                self.user_number_index[user_number] = user

    def all(self):
        """Retrieve all users."""
        return list(self.user_id_index.values())

    def find_by_id(self, user_id):
        """Perform a lookup by user_id."""
        if user_id in self.user_id_index:
            return self.user_id_index[user_id]
        else:
            return None

    def find_by_number(self, user_number):
        """Perform a lookup by user_number."""
        if user_number in self.user_number_index:
            return self.user_number_index[user_number]
        else:
            return None

    def add(self, user_id, rights, name, email):
        user_numbers_list = list(self.user_number_index.keys())
        next_user_number = get_next_number(user_numbers_list[-1])
        padded_user_number = "{:06d}".format(next_user_number)
        shash = "generichash"
        entry = "{}:{}:{}:{}:{}:{}\n".format(
            user_id, padded_user_number, shash, rights, name, email)

        users_file_path = os.path.join('app', 'db', 'users.txt')
        temp_path = 'users.tmp'
        copy2(users_file_path, temp_path)
        with open(temp_path, 'a') as temp_file:
            temp_file.write(entry)
        os.rename(temp_path, users_file_path)

        user = user_dict(
            user_id, padded_user_number, shash, rights, name, email
        )
        self.user_id_index[user_id] = user
        self.user_number_index[padded_user_number] = user
        return user

    def update(self, user_number, user_id, rights, name, email):
        pass


class TranscriptStore():
    """
    Transcript Storage and Management.

    TODO:
    - Constructor
    - Find transcripts by users
    - Find transcripts for prompt

    """

    def __init__(self):
        transcripts_path = os.path.join('app', 'db')
        self.transcripts = {file[:-4] for file in os.listdir(transcripts_path)
                            if is_transcript_file(file)}

    def add_transcription(self, user_number, recording_id, transcript):
        latest_transcript_id = max(
            [transcript_id for transcript_id in self.transcripts
             if transcript_of_recording(transcript_id, recording_id)])
        next_transcript_id = get_next_number(latest_transcript_id[-3:])
        transcript_file_name = '{}n{:03d}.txt'.format(
            recording_id, next_transcript_id)
        transcript_file_path = os.path.join('app', 'db', transcript_file_name)
        with open(transcript_file_path, 'w') as f:
            f.write(transcript)
        prompt_id, student_id = recording_id[1:].split("s")
        transcript_history_file = os.path.join(
            'app', 'db', 'u{}.txt'.format(user_number))
        with open(transcript_history_file, 'a') as f:
            f.write("{} {} {}\n".format(prompt_id,
                                        student_id, next_transcript_id))

    def transcribed_by_user(self, user_number):
        transcribed_recordings = set()
        user_file_path = os.path.join('app', 'db', 'u{}.txt'.format(user_number))
        with open(user_file_path, 'r') as completed_transcripts_file:
            for line in completed_transcripts_file:
                fields = tuple(line.strip().split(" "))
                transcribed_recordings.add("p{}s{}".format(*fields))
        return transcribed_recordings


class PromptStore():
    """Prompt Storage and Management."""

    def __init__(self):
        prompts_path = os.path.join('app', 'db')
        self.prompt_ids = {file[1:-4] for file in os.listdir(prompts_path)
                           if is_prompt_file(file)}

    def find_by_id(self, prompt_id):
        if prompt_id not in self.prompt_ids:
            return None
        prompt_file = "p{}.txt".format(prompt_id)
        prompt_file_path = os.path.join('app', 'db', prompt_file)

        with open(prompt_file_path, 'r') as f:
            return f.read()

    def add(self, text):
        latest_prompt_id = max(self.prompt_ids)
        next_prompt_id = get_next_number(latest_prompt_id)
        prompt_file_name = 'p{:06d}.txt'.format(next_prompt_id)
        prompt_file_path = os.path.join('app', 'db', prompt_file_name)
        with open(prompt_file_path, 'w') as f:
            f.write(text)

    def retrieve_random_unvoiced_prompt(self, user_number):
        voiced_prompts = recordings.recordings_by_user(user_number)
        unvoiced_prompts = list(self.prompt_ids - voiced_prompts)

        random_prompt = choice(unvoiced_prompts)
        return {"prompt_id": random_prompt,
                "text": self.find_by_id(random_prompt)}


class RecordingStore():
    """Recording Storage and Management."""

    def __init__(self):
        recordings_path = os.path.join('app', 'db')
        self.recordings = {file[:-4] for file in os.listdir(recordings_path)
                           if is_recording(file)}

    def add(self, user_number, prompt_id, recording_file):
        recording_file_name = 'p{}s{}.mp3'.format(prompt_id, user_number)
        recording_file.save(os.path.join('app', 'db', recording_file_name))

        return recording_file_name

    def recordings_by_user(self, user_number):
        return {recording for recording in self.recordings
                if recorded_by_user(recording, user_number)}

    def retrieve_random_untranscribed_recording(self, user_number):
        completed_recordings = transcripts.transcribed_by_user(user_number)
        untranscribed_recordings = list(self.recordings - completed_recordings)
        random_recording = choice(untranscribed_recordings)
        return random_recording

    def download_recording(self, recording_id):
        recordings_file_path = os.path.join('db', "{}.mp3".format(recording_id))
        return send_file(recordings_file_path)

users = UserStore()
transcripts = TranscriptStore()
prompts = PromptStore()
recordings = RecordingStore()
