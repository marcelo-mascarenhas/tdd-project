from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Token
from unittest.mock import patch

User = get_user_model()

class UserModelTest(TestCase):

    def test_user_is_valid_with_email_only(self):
        user = User(email='a@b.com')
        user.full_clean()  # should not raise

    def test_email_is_primary_key(self):
        user = User(email='a@b.com')
        self.assertEqual(user.pk, 'a@b.com')


class TokenModelTest(TestCase):

    def test_links_user_with_auto_generated_uid(self):
        token1 = Token.objects.create(email='a@b.com')
        token2 = Token.objects.create(email='a@b.com')
        self.assertNotEqual(token1.uid, token2.uid)


class SendLoginEmailViewTest(TestCase):
    
    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        })

        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'noreply@superlists')
        self.assertEqual(to_list, ['edith@example.com'])