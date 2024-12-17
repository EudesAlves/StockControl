import hashlib
import random
import string
from app_login.models import Login
from app_login.models import User

class LoginUtil():
    def generate_password_hash(password, hash_word):
        encoded = hashlib.md5(password.encode('utf-8') + hash_word.encode('utf-8')).hexdigest()
        return encoded

    def generate_random_hash():
        random_size = random.randint(5,9)
        return ''.join(random.choice(string.ascii_letters) for x in range(random_size))
    
    def is_logged(request):
        if 'user_id' in request.session:
            return True
        return False

    def populate_initial_login():
        logins = Login.objects.all()
        if logins.count() == 0:
            login = Login()
            user = User()
            TEST_NAME = "Teste"
            TEST_EMAIL = "teste@teste.com"
            TEST_PASS = "teste"

            random_hash = LoginUtil.generate_random_hash()
            login.email = TEST_EMAIL
            login.random_hash = random_hash
            login.password = LoginUtil.generate_password_hash(TEST_PASS, random_hash)
            login.save()
            login_id = (Login.objects.last()).id

            user.name = TEST_NAME
            user.email = TEST_EMAIL
            user.login_id = login_id
            user.save()