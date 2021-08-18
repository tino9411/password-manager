import psycopg2
from hashlib import sha256
import encryption

def get_hexdigest(salt, text):
    salt = salt.encode('utf-8')
    text = text.encode('utf-8')
    return sha256(salt + text).hexdigest()

key = encryption.EncryptDecrypt()
SECRET_KEY = key.load_key().decode()

def hash_password(text):
    salt = get_hexdigest(text, SECRET_KEY)[:20]
    hash = get_hexdigest(text, salt)
    return ''.join((salt, hash))

ALPHABET = ('abcdefghikjlmnopqrstuvwxyz'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            '0123456789!@£$%^&*()-_')

def set_password(text, length=10, alphabet=ALPHABET):
    raw_hexdigest = hash_password(text)

    # Convert the hexidigest into decimal
    num = int(raw_hexdigest, 16)

    # What base will we convert 'num' into?
    num_chars=len(alphabet)

    # Build up the new password one "digit" at a time,
    # up to a certain length

    chars = []
    while len(chars) < length:
        num, i = divmod(num, num_chars)
        chars.append(alphabet[i])

    return ''.join(chars)