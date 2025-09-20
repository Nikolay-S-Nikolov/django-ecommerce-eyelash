from django.test import TestCase
from lash_store.contact.forms import ContactForm

class ContactFormTests(TestCase):

    def test__valid_form_data(self):
        form_data = {
            'email': 'user@example.com',
            'name': 'Иван Иванов',
            'message': 'Здравейте, имам въпрос.'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_email(self):
        form_data = {
            'name': 'Иван',
            'message': 'Няма email'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_invalid_email_format(self):
        form_data = {
            'email': 'invalid-email',
            'name': 'Иван',
            'message': 'Невалиден email'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_empty_message(self):
        form_data = {
            'email': 'user@example.com',
            'name': 'Иван',
            'message': ''
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)
