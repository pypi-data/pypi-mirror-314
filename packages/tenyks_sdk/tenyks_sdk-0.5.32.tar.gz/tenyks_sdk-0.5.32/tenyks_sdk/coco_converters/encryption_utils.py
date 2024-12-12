import hashlib


def sha224_encrypt(message):
    encrypted_message_string = hashlib.sha224(message.encode("utf-8")).hexdigest()

    return encrypted_message_string
