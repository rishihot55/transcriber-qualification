import re


def user_dict(user_id, user_number, shash, rights, name, email):
    """A helper function to format the user data."""
    return {
        'user_id': user_id,
        'user_number': user_number,
        'rights': rights,
        'name': name,
        'email': email
    }


def get_next_number(padded_num):
    next_num = int(padded_num.lstrip("0")) + 1
    return next_num


def is_prompt_file(filename):
    prompt_pattern = re.compile('^p[0-9]{6}\.txt$')
    return bool(prompt_pattern.match(filename))


def is_recording(filename):
    recording_pattern = re.compile('^p[0-9]{6}s[0-9]{6}\.(mp3|wav)$')
    return bool(recording_pattern.match(filename))
