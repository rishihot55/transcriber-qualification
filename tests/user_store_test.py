from app.helpers.data import UserStore
from app.helpers.exceptions import UniqueConstraintError, StoreError
from tests.helpers import data_path, seed_users_db, rm


import os
import unittest


class UserStoreTestCase(unittest.TestCase):
    """Test cases for the UserStore class."""

    def setUp(self):
        """Setup using seed `users.txt`."""
        self.users_file = os.path.join(data_path, 'users.txt')
        seed_users_db(self.users_file)
        self.users = UserStore(data_path)

    def tearDown(self):
        """Remove users file."""
        rm(self.users_file)

    def test_find_valid_user_by_id(self):
        user_id = 'sample_admin'
        user = self.users.find_by_id(user_id)
        self.assertEqual(user['user_id'], user_id)

    def test_find_nonexistent_user_by_id(self):
        nonexistent_id = 'nonexistent_id'
        nonexistent_user = self.users.find_by_id(nonexistent_id)
        self.assertIsNone(nonexistent_user)

    def test_find_valid_user_by_number(self):
        user_number = '000001'
        user = self.users.find_by_number(user_number)
        self.assertEqual(user['user_number'], user_number)

    def test_find_nonexistent_user_by_number(self):
        nonexistent_user_number = '100000'
        nonexistent_user = self.users.find_by_number(
            nonexistent_user_number)
        self.assertIsNone(nonexistent_user)

    def test_find_valid_user_by_email(self):
        user_email = 'voicer@voicer.com'
        user = self.users.find_by_email(user_email)
        self.assertEqual(user['email'], user_email)

    def test_find_nonexistent_user_by_email(self):
        nonexistent_email = 'invalid@email.com'
        nonexistent_user = self.users.find_by_email(
            nonexistent_email)
        self.assertIsNone(nonexistent_user)

    def test_add_new_user(self):
        next_id = '000004'
        valid_user_data = (
            "test_voicer", "001", "Test Voicer", "test@voicer.com")
        new_user = self.users.add(*valid_user_data)
        self.assertEqual(new_user['user_number'], next_id)

    def test_duplicate_user_data(self):
        duplicate_id_user_data = (
            "sample_voicer", "001", "Sample Voicer", "sample@voicer.com")

        with self.assertRaises(UniqueConstraintError):
            self.users.add(*duplicate_id_user_data)

        duplicate_email_user_data = (
            "v", "001", "Voicer", "voicer@voicer.com")

        with self.assertRaises(UniqueConstraintError):
            self.users.add(*duplicate_email_user_data)

    def test_add_non_setup_userstore(self):
        """Throw a StoreError if users file doesn't exist."""
        os.remove(self.users_file)
        user_data = (
            "test_voicer", "001", "Test Voicer", "test@voicer.com")
        with self.assertRaises(StoreError):
            self.users.add(*user_data)
