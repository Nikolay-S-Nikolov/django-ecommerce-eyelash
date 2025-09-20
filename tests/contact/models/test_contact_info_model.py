from django.test import TestCase
from lash_store.contact.models import ContactInfo

class ContactInfoTest(TestCase):
    def setUp(self):
        self.contact_data = {
        'phone_number':'+359888123456',
        'working_time':'Пон-Пет: 09:00 - 18:00',
        'address':'ул. Примерна 123, София',
        'custom_message':'Очакваме ви!',
        }

    def test__contact_info_creation(self):
        contact = ContactInfo.objects.create(**self.contact_data)

        self.assertEqual(contact.phone_number, '+359888123456')
        self.assertEqual(contact.working_time, 'Пон-Пет: 09:00 - 18:00')
        self.assertEqual(contact.address,'ул. Примерна 123, София')
        self.assertTrue(contact.visible)

    def test__contact_info_str_representation(self):
        contact = ContactInfo.objects.create(**self.contact_data)
        expected = "Информация за контакти тел:+359888123456 създадена на"
        self.assertIn(expected, str(contact))

