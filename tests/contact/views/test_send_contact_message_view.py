from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

class SendContactMessageViewTests(TestCase):

    def setUp(self):
        self.url = reverse('send_contact_message')  # увери се, че URL е зададен така

    @patch('lash_store.contact.views.send_mail')
    def test__valid_contact_form_sends_email(self, mock_send_mail):
        data = {
            'name': 'Иван Иванов',
            'email': 'ivan@example.com',
            'message': 'Здравейте, имам въпрос.'
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'success': True, 'message': 'Съобщението е изпратено успешно!'}
        )

        mock_send_mail.assert_called_once()
        args, kwargs = mock_send_mail.call_args
        self.assertIn('Ново съобщение от Иван Иванов (ivan@example.com)', args)
        self.assertIn('Здравейте, имам въпрос.', kwargs['message'])
        self.assertEqual(kwargs['from_email'], 'ivan@example.com')

    def test_invalid_contact_form_returns_errors(self):
        data = {
            'name': '',
            'email': 'невалиден-email',
            'message': ''
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()

        self.assertFalse(json_data['success'])
        self.assertIn('email', json_data['errors'])
        self.assertIn('name', json_data['errors'])
        self.assertIn('message', json_data['errors'])
