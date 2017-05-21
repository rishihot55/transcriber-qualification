"""Data Management Helpers."""
import os
from app.helpers.format import user_dict


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
        last_user_number = user_numbers_list[-1].lstrip("0")
        next_user_number = int(last_user_number) + 1
        padded_user_number = "{:06d}".format(next_user_number)
        shash = "generichash"
        entry = "{}:{}:{}:{}:{}:{}\n".format(
            user_id, padded_user_number, shash, rights, name, email)
        users_file_path = os.path.join('app', 'db', 'users.txt')
        with open(users_file_path, 'a') as users_file:
            users_file.write(entry)
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
        """Get a prompt-wise last transcript index."""
        # TODO
        pass


class PromptStore():
    """Prompt Storage and Management."""

    def __init__(self):
        """Get the last prompt index."""
        # TODO
        pass


class RecordingStore():
    """Recording Storage and Management."""

    def __init__(self):
        """Get latest prompt-wise recording index."""
        pass

users = UserStore()
transcripts = TranscriptStore()
prompts = PromptStore()
recordings = RecordingStore()
