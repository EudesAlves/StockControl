import hashlib
import random
import string

class LoginUtil():
    def generate_password_hash(password, hash_word):
        encoded = hashlib.md5(password.encode('utf-8') + hash_word.encode('utf-8')).hexdigest()
        return encoded

    def generate_random_hash():
        random_size = random.randint(5,9)
        return ''.join(random.choice(string.ascii_letters) for x in range(random_size))