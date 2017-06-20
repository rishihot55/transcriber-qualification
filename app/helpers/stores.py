from app.helpers.data import UserStore, TranscriptStore
from app.helpers.data import PromptStore, RecordingStore

import os

data_path = os.path.join('app', 'db')

users = UserStore(data_path)
transcripts = TranscriptStore(data_path)
prompts = PromptStore(data_path)
recordings = RecordingStore(data_path)
