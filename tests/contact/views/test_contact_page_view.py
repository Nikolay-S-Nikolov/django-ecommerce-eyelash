from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from lash_store.contact.models import ContactInfo, SocialLink
from lash_store.contact.forms import ContactForm

User = get_user_model()

class ContactPageViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('contact-page')

        self.contact_info = ContactInfo.objects.create(
            phone_number='+359888123456',
            working_time='Пон-Пет: 09:00 - 18:00',
            address='ул. Примерна 123',
            custom_message='Очакваме ви!',
            visible=True
        )

        self.social_link = SocialLink.objects.create(
            label='Facebook',
            url='https://facebook.com/example',
            icon_class='fa-facebook',
            appearance_order=1
        )

    def test__contact_page_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test__contact_page_context_contains_contact_info_and_links(self):
        response = self.client.get(self.url)
        self.assertIn('contact_info', response.context)
        self.assertIn('links', response.context)
        self.assertEqual(response.context['contact_info'], self.contact_info)
        self.assertIn(self.social_link, response.context['links'])

    def test__contact_page_form_is_instance_of_contact_form(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], ContactForm)

    def test__get_initial_for_authenticated_user(self):
        user = User.objects.create_user(email='user@example.com', password='not_password')
        user.profile.phone_number = '0888000000'
        user.profile.save()

        self.client.login(email='user@example.com', password='not_password')
        response = self.client.get(self.url)
        form = response.context['form']
        self.assertEqual(form.initial['email'], 'user@example.com')
        self.assertEqual(form.initial['phone'], '0888000000')
