from django.test import TestCase

# Create your tests here.
from base.tests import BaseTestCase
from users.models import Account


class UserTestCase(BaseTestCase):

    def test_account_subscription(self):
        account = Account.objects.get(email='elijah.kane.1972@gmail.com')
        self.assertFalse(account.subscription())

    def test_create_account(self):
        account = Account.objects.create_user(
            "test_user@gmail.com",
            "test_user",
            "test_user",
            "test_user",
            "test_password"
        )
        self.assertEqual(Account.objects.count(), 3)