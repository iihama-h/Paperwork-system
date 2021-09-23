from django.contrib.auth import get_user_model
from django.test import TestCase


# loginを前提とする処理用のテストクラス
class LoggedInTestCase(TestCase):

    def setUp(self):

        self.id = 1
        self.username = 'test_user'
        self.email = 'test@test.com'
        self.password = 'password'

        self.test_user = get_user_model().objects.create_user(
            id=self.id,
            username=self.username,
            email=self.email,
            password=self.password)

        self.client.login(username=self.username, password=self.password)
