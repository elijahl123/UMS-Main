from django.test import TestCase

# Create your tests here.
from users.models import Account


class UserTestCase(TestCase):
    def setUp(self):
        Account.objects.create_user(
            email='elijah.kane.1972@gmail.com',
            username='elijahl123',
            first_name='Elijah',
            last_name='Lopez',
            password='password'
        )

    def test_account_subscription(self):
        account = Account.objects.get(email='elijah.kane.1972@gmail.com')
        self.assertTrue(account.subscription())