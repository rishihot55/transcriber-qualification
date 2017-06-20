from app.helpers.format import is_prompt_file, is_recording

import os
import shutil

data_path = os.path.join('tests', 'db')
seed_path = os.path.join('tests', 'seed')


def touch(file_path):
    """Create an empty file, if it doesn't exist."""
    open(file_path, 'a').close()


def list_prompts(path):
    """List all prompts in the directory."""
    return [file for file in os.listdir(path) if is_prompt_file(file)]


def list_recordings(path):
    """List all recordings in the directory."""
    return [file for file in os.listdir(path) if is_recording(file)]


def seed_users_db(dest):
    """Load seed user data to test data store."""
    seed_users_file = os.path.join(seed_path, 'users.txt')
    shutil.copy2(seed_users_file, dest)


def seed_prompts(dest):
    """Copy seed prompt files to test data store."""
    prompt_files = list_prompts(seed_path)
    for file in prompt_files:
        seed_prompt_file = os.path.join(seed_path, file)
        destination_file = os.path.join(dest, file)
        shutil.copy2(seed_prompt_file, destination_file)


def seed_recordings(dest):
    """Copy seed recording files to test data store."""
    recordings = list_recordings(seed_path)
    for file in recordings:
        seed_recording = os.path.join(seed_path, file)
        destination_file = os.path.join(dest, file)
        shutil.copy2(seed_recording, destination_file)


def clear_recordings(path):
    for file in list_recordings(path):
        rm(os.path.join(path, file))


def clear_prompts(path):
    for file in list_prompts(path):
        rm(os.path.join(path, file))

def rm(file):
    """Remove files if present."""
    if os.path.isfile(file):
        os.remove(file)
