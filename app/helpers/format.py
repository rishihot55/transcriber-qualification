import re
import magic


def user_dict(user_id, user_number, shash, rights, name, email):
    """A helper function to format the user data."""
    return {
        'user_id': user_id,
        'user_number': user_number,
        'rights': rights,
        'name': name,
        'email': email
    }


def serialize_user(user_id, user_number, shash, rights, name, email):
    return "{}:{}:{}:{}:{}:{}\n".format(user_id, user_number, shash, rights, name, email)

def get_next_number(padded_num):
    next_num = int(padded_num.lstrip("0")) + 1
    return next_num


def parse_prompt_id(file):
    return file[1:7]


def is_prompt_file(filename):
    prompt_pattern = re.compile('^p[0-9]{6}\.txt$')
    return bool(prompt_pattern.match(filename))


def is_recording(filename):
    recording_pattern = re.compile('^p[0-9]{6}s[0-9]{6}\.(mp3|wav)$')
    return bool(recording_pattern.match(filename))


def is_transcript_file(filename):
    transcript_pattern = re.compile('^p[0-9]{6}s[0-9]{6}n[0-9]{3}\.txt$')
    return bool(transcript_pattern.match(filename))


def is_audio_file(file):
    mime_type = file.content_type
    return mime_type in ['audio/mp3', 'audio/wav']


def transcript_of_recording(transcript_id, recording_id):
    return recording_id in transcript_id


def recorded_by_user(recording_id, user_number):
    return 's' + user_number in recording_id


def clean_transcript(transcript):
    """Process punctuation and other symbols and normalize to lower case."""
    punctuation_stripped_transcript = re.sub(r'[^\w\']', " ", transcript)
    cleaned_transcript = re.sub(r'\s+', " ",
                                punctuation_stripped_transcript).strip().lower()
    return cleaned_transcript
