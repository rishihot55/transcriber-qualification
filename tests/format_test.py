from app.helpers import format

import unittest


class FormatTestCase(unittest.TestCase):
    def test_valid_prompt_files(self):
        prompt_files = ["p000001.txt", "p000100.txt", "p401234.txt"]
        filtered_files = list(filter(format.is_prompt_file, prompt_files))

        assert prompt_files == filtered_files

    def test_invalid_prompt_files(self):
        """Ensure filter doesn't pick up any other files."""
        invalid_files = [
            "p01.txt",
            "abc.txt",
            "p000001s000001.mp3",
            "p000001s000001n001.txt",
            "u000001.txt"
        ]
        filtered_files = list(filter(format.is_prompt_file, invalid_files))

        assert len(filtered_files) == 0

    def test_valid_recording_files(self):
        recording_files = [
            "p000001s000001.mp3",
            "p000001s000003.wav",
            "p000502s000030.mp3"
        ]

        filtered_files = list(filter(format.is_recording, recording_files))

        assert recording_files == filtered_files

    def test_invalid_recording_files(self):
        invalid_files = [
            "p000001s000001.mp4",
            "p000001s00001.mp3",
            "p000001s000001n001.txt",
            "u000001.txt",
            "p000002.txt"
        ]

        filtered_files = list(filter(format.is_recording, invalid_files))

        assert len(filtered_files) == 0

    def test_valid_transcript_file(self):
        transcript_files = [
            "p000001s000001n001.txt",
            "p000001s000001n011.txt",
            "p000102s000301n001.txt"
        ]

        filtered_files = list(filter(format.is_transcript_file, transcript_files))

        assert transcript_files == filtered_files

    def test_invalid_transcript_files(self):
        invalid_files = [
            "p00001s000001n011.txt",
            "p000001s000001n01.txt",
            "p000001s00001n011.txt",
            "u000001.txt",
            "p000002.txt",
            "p000001s000001.mp3",
            "p000001s000003.wav",
            "p000502s000030.mp3"
        ]

        filtered_files = list(filter(format.is_transcript_file, invalid_files))

        assert len(filtered_files) == 0

    def test_clean_transcripts(self):
        transcripts = [
            "We drank tea in the afternoon and watched TV.",
            "Wheres your TV, I dont know im watvhing the TV.",
            "We stayed in in the afternoon amd watched tv."
        ]

        cleaned_transcripts = list(map(format.clean_transcript, transcripts))

        expected_transcripts = [
            "we drank tea in the afternoon and watched tv",
            "wheres your tv i dont know im watvhing the tv",
            "we stayed in in the afternoon amd watched tv"
        ]

        assert expected_transcripts == cleaned_transcripts


if __name__ == '__main__':
    unittest.main()
