from app.helpers.data import PromptStore, UserStore, RecordingStore
from tests.helpers import data_path, rm, list_prompts
from tests.helpers import seed_users_db, seed_prompts, seed_recordings
from tests.helpers import clear_recordings, clear_prompts
import os
import unittest
import random


class PromptStoreTestCase(unittest.TestCase):
    def setUp(self):
        """Copy users file and prompts to directory."""
        self.users_file = os.path.join(data_path, 'users.txt')
        seed_prompts(data_path)
        seed_recordings(data_path)
        seed_users_db(self.users_file)

        self.users = UserStore(data_path)
        self.prompts = PromptStore(data_path)
        self.recordings = RecordingStore(data_path)

    def tearDown(self):
        """Remove the users file and prompts."""
        rm(self.users_file)
        clear_prompts(data_path)
        clear_recordings(data_path)

    def test_all(self):
        """Test retrieval of prompts."""
        expected_prompts = {
            "000001": "We drank tea in the afternoon and watched TV.",
            "000002": "Are you a leader or a follower?",
            "000003": "Sticks and stones won't break my bones"}
        fetched_prompts = self.prompts.all()
        self.assertEqual(fetched_prompts, expected_prompts)

    def test_add(self):
        """Test addition of a new prompt."""
        new_file = "p000004.txt"
        self.prompts.add("Arbitrary content")
        prompt_files = list_prompts(data_path)
        self.assertIn(new_file, prompt_files)

    def test_retrieve_random_unvoiced_prompt(self):
        random.seed(666)
        prompt = self.prompts.retrieve_random_unvoiced_prompt(
            self.recordings, '000001')
        self.assertEqual(
            prompt['text'], "Sticks and stones won't break my bones")

    def test_all_prompts_voiced(self):
        prompt = self.prompts.retrieve_random_unvoiced_prompt(
            self.recordings, '000003')
        self.assertEqual(prompt['prompt_id'], -1)
