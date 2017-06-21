"""Data Management Helpers."""
import os
import re
from shutil import copy2
from app.helpers.format import get_next_number, is_prompt_file, parse_prompt_id
from app.helpers.format import user_dict, is_recording, serialize_user
from app.helpers.format import transcript_of_recording, is_transcript_file
from app.helpers.format import recorded_by_user
from app.helpers.exceptions import UniqueConstraintError, StoreError
from random import choice
from flask import send_from_directory


class UserStore():
    """User Storage and Management."""

    def __init__(self, data_path):
        """
        Load the data from the flat file.

        TODO:
        - Add method
        - Update method
        """
        self.user_id_index = {}
        self.user_number_index = {}
        self.user_email_index = {}
        self.users_file_path = os.path.join(data_path, 'users.txt')
        with open(self.users_file_path, 'r') as users_file:
            for line in users_file:
                values = line.strip().split(":")
                (user_id, user_number, shash, rights, name, email) = values
                user = user_dict(
                    user_id, user_number, shash, rights, name, email
                )
                self.user_id_index[user_id] = user
                self.user_number_index[user_number] = user
                self.user_email_index[email] = user

    def all(self):
        """Retrieve all users."""
        return list(self.user_id_index.values())

    def find_by_id(self, user_id):
        """Perform a lookup by user_id."""
        return self.user_id_index.get(user_id, None)

    def find_by_number(self, user_number):
        """Perform a lookup by user_number."""
        return self.user_number_index.get(user_number, None)

    def find_by_email(self, email):
        """Perform a lookup by email address."""
        return self.user_email_index.get(email, None)

    def __next_user_number(self):
        user_numbers_list = list(self.user_number_index.keys())
        latest_user_number = max(user_numbers_list)
        next_user_number = get_next_number(latest_user_number)
        padded_user_number = "{:06d}".format(next_user_number)
        return padded_user_number

    def __save_entry(self, entry):
        temp_path = 'users.tmp'
        copy2(self.users_file_path, temp_path)
        with open(temp_path, 'a') as temp_file:
            temp_file.write(entry)
        os.rename(temp_path, self.users_file_path)

    def add(self, user_id, rights, name, email):
        """Insert a new user into the store."""
        if self.find_by_id(user_id) or self.find_by_email(email):
            raise UniqueConstraintError
        next_user_number = self.__next_user_number()
        shash = "generichash"
        entry = serialize_user(
            user_id, next_user_number, shash, rights, name, email)
        try:
            self.__save_entry(entry)
        except (IOError, FileNotFoundError):
            raise StoreError
        user = user_dict(
            user_id, next_user_number, shash, rights, name, email
        )
        self.user_id_index[user_id] = user
        self.user_number_index[next_user_number] = user
        return user

    def __update_contents(self, content, entry):
        user_number = entry[1]
        pattern = '\\b.*?:{}.*?\n'.format(user_number)
        updated_contents = re.sub(pattern, entry, content)
        return updated_contents

    def __save_content(self, content):
        temp_path = 'users.tmp'
        with open(temp_path, 'w') as temp_file:
            temp_file.write(content)
        os.rename(temp_path, self.users_file_path)

    def update(self, user_number, user_id, rights, name, email):
        """Update an existing user in the store."""
        users_content = None
        with open(self.users_file_path, 'r') as f:
            users_content = f.read()
        shash = "generichash"
        entry = serialize_user(
            user_id, user_number, shash, rights, name, email)
        updated_contents = self.__update_contents(users_content, entry)
        self.__save_content(updated_contents)
        user = user_dict(
            user_id, user_number, shash, rights, name, email
        )
        self.user_id_index[user_id] = user
        self.user_number_index[user_number] = user
        return user


class TranscriptStore():
    """
    Transcript Storage and Management.

    TODO:
    - Find transcripts for prompt

    """

    def __init__(self, data_path):
        """Load list of transcripts into an index."""
        self.transcripts_path = data_path
        self.transcripts = {
            file[:-4] for file in os.listdir(self.transcripts_path)
            if is_transcript_file(file)}

    def __new_id(self, recording_id):
        transcript_id_list = [
            transcript_id for transcript_id in self.transcripts
            if transcript_of_recording(transcript_id, recording_id)]

        if len(transcript_id_list) > 0:
            latest_transcript_id = max(transcript_id_list)
            next_transcript_id = get_next_number(latest_transcript_id[-3:])
        else:
            next_transcript_id = 1

        return next_transcript_id

    def __save_transcript(self, recording_id, next_transcript_id, transcript):
        transcript_file_name = '{}n{:03d}.txt'.format(recording_id,
                                                      next_transcript_id)
        transcript_file_path = os.path.join(
            self.transcripts_path, transcript_file_name)
        with open(transcript_file_path, 'w') as f:
            f.write(transcript)
        return transcript_file_name

    def __add_to_history(self, user_number, recording_id, next_transcript_id):
        prompt_id, student_id = recording_id[1:].split("s")
        transcript_history_file = os.path.join(
            self.transcripts_path, 'u{}.txt'.format(user_number))
        with open(transcript_history_file, 'a') as f:
            f.write("{} {} {}\n".format(prompt_id,
                                        student_id, next_transcript_id))

    def add(self, user_number, recording_id, transcript):
        """Add a new transcription of a recording by a user."""
        next_transcript_id = self.__new_id(recording_id)
        transcript_file_name = self.__save_transcript(recording_id,
                                                      next_transcript_id,
                                                      transcript)
        self.__add_to_history(user_number, recording_id, next_transcript_id)
        self.transcripts.add(transcript_file_name[:-4])

    def transcribed_by_user(self, user_number):
        """Retrieve all recordings transcribed by a given user."""
        transcribed_recordings = set()
        user_file_path = os.path.join(
            self.transcripts_path, 'u{}.txt'.format(user_number))
        if not os.path.isfile(user_file_path):
            open(user_file_path, 'w').close()
        with open(user_file_path, 'r') as completed_transcripts_file:
            for line in completed_transcripts_file:
                fields = tuple(line.strip().split(" "))
                transcribed_recordings.add("p{}s{}".format(*fields))
        return transcribed_recordings


class PromptStore():
    """Prompt Storage and Management."""

    def __init__(self, data_path):
        """Load all prompts from disk and create an index in memory."""
        self.prompts_path = data_path
        self.prompt_ids = {parse_prompt_id(file)
                           for file in os.listdir(self.prompts_path)
                           if is_prompt_file(file)}
        self.prompts = {}
        for prompt_id in self.prompt_ids:
            prompt_file = "p{}.txt".format(prompt_id)
            prompt_file_path = os.path.join(self.prompts_path, prompt_file)
            with open(prompt_file_path, 'r') as f:
                self.prompts[prompt_id] = f.read()

    def all(self):
        """Return all prompts."""
        return self.prompts

    def find_by_id(self, prompt_id):
        """Find a given prompt by id."""
        return self.prompts[prompt_id]

    def __new_id(self):
        if len(self.prompt_ids):
            latest_prompt_id = max(self.prompt_ids)
            next_prompt_id = get_next_number(latest_prompt_id)
        else:
            next_prompt_id = 1
        return next_prompt_id

    def __save(self, new_prompt_id, text):
        prompt_file_name = 'p{:06d}.txt'.format(new_prompt_id)
        prompt_file_path = os.path.join(self.prompts_path, prompt_file_name)
        with open(prompt_file_path, 'w') as f:
            f.write(text)
        return prompt_file_name

    def add(self, text):
        """Add a new prompt."""
        next_prompt_id = self.__new_id()
        prompt_file_name = self.__save(next_prompt_id, text)
        self.prompt_ids.add(parse_prompt_id(prompt_file_name))
        self.prompts["{:06d}".format(next_prompt_id)] = text

    def __voiced_prompts_by_user(self, recording_store, user_number):
        return {
            parse_prompt_id(recording) for recording
            in recording_store.recordings_by_user(user_number)}

    def retrieve_random_unvoiced_prompt(self, recording_store, user_number):
        """
        Retrieve a random chosen prompt which hasn't been voiced by the user.
        """
        voiced_prompts = self.__voiced_prompts_by_user(
            recording_store, user_number)
        unvoiced_prompts = sorted(list(self.prompt_ids - voiced_prompts))
        if unvoiced_prompts:
            random_prompt = choice(unvoiced_prompts)
            return {"prompt_id": random_prompt,
                    "text": self.find_by_id(random_prompt)}
        else:
            return {"prompt_id": -1, "text": ""}


class RecordingStore():
    """Recording Storage and Management."""

    def __init__(self, data_path):
        """Load recordings to memory."""
        self.recordings_path = data_path
        self.recordings = {
            file[:-4] for file in os.listdir(self.recordings_path)
            if is_recording(file)}

    def add(self, user_number, prompt_id, recording_file):
        """Save a new recording to disk."""
        recording_file_name = 'p{}s{}.mp3'.format(prompt_id, user_number)
        recording_file.save(
            os.path.join(self.recordings_path, recording_file_name))
        self.recordings.add(recording_file_name[:-4])
        return recording_file_name

    def all(self):
        """Retrieve list of recordings."""
        return self.recordings

    def exists(self, recording_id):
        """Test if a given recording exists."""
        return recording_id in self.recordings

    def recordings_by_user(self, user_number):
        """Retrieve all recordings voiced by a user."""
        return {recording for recording in self.recordings
                if recorded_by_user(recording, user_number)}

    def retrieve_random_untranscribed_recording(self, transcript_store, user_number):
        """
        Retrieve a random recording whose prompt hasn't
        been transcribed by the user.
        """
        completed_recordings = transcript_store.transcribed_by_user(
            user_number)
        completed_prompts = {parse_prompt_id(recording)
                             for recording in completed_recordings}
        prompts_with_recordings = {parse_prompt_id(recording)
                                   for recording in self.recordings}
        untranscribed_prompts = list(
            prompts_with_recordings - completed_prompts)
        if untranscribed_prompts:
            random_prompt = choice(untranscribed_prompts)
            recordings_of_prompt = [
                recording for recording in self.recordings
                if parse_prompt_id(recording) == random_prompt]
            random_recording = choice(recordings_of_prompt)
            return random_recording
        else:
            return -1

    def download_recording(self, recording_id):
        """Retrieve a recording from disk."""
        return send_from_directory(
            os.path.join('..', self.recordings_path),
            "{}.mp3".format(recording_id))
