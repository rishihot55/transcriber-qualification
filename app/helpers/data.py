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
