from django.test import TestCase
from django.urls import reverse
from lash_store.contact.models import ContactInfo, SocialLink

class ContactTemplateTests(TestCase):

    def setUp(self):
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

    def test__template_renders_successfully(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact_page.html')

    def test__template_contains_contact_info(self):
        response = self.client.get(self.url)
        content = response.content.decode()

        self.assertIn('Свържете се с нас', content)
        self.assertIn(self.contact_info.phone_number, content)
        self.assertIn(self.contact_info.address, content)
        self.assertIn(self.contact_info.custom_message, content)
        self.assertIn('Работно време:', content)

    def test__template_contains_social_links(self):
        response = self.client.get(self.url)
        content = response.content.decode()

        self.assertIn(self.social_link.url, content)
        self.assertIn(self.social_link.icon_class, content)

    def test__template_contains_form_fields(self):
        response = self.client.get(self.url)
        content = response.content.decode()

        self.assertIn('name="email"', content)
        self.assertIn('name="name"', content)
        self.assertIn('name="message"', content)
        self.assertIn('Изпрати', content)

    def test__template_contains_spinner_and_script(self):
        response = self.client.get(self.url)
        content = response.content.decode()

        self.assertIn('id="form-spinner"', content)
        self.assertIn('fa-spinner fa-spin', content)
        self.assertIn('js/send_message.js', content)
