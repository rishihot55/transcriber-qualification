from app.helpers.data import UserStore, TranscriptStore
from app.helpers.data import PromptStore, RecordingStore

import os

data_path = os.path.join('app', 'db')
hit_data_path = os.path.join('app', 'hit_db')

users = UserStore(data_path)
transcripts = TranscriptStore(data_path)
prompts = PromptStore(data_path)
recordings = RecordingStore(data_path)

hit_prompts = PromptStore(hit_data_path)
hit_recordings = RecordingStore(hit_data_path)
hit_transcripts = TranscriptStore(hit_data_path)
