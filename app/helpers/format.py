def user_dict(user_id, user_number, shash, rights, name, email):
    """A helper function to format the user data."""
    return {
        'user_id': user_id,
        'user_number': user_number,
        'rights': rights,
        'name': name,
        'email': email
    }
