from django.test import TestCase
from lash_store.contact.models import SocialLink

class SocialLinkModelTests(TestCase):
    def test__social_link_creation_with_predefined_icon(self):
        link = SocialLink.objects.create(
            label='Нашата Facebook страница',
            url='https://facebook.com/example',
            icon_class='fa-facebook',
            appearance_order=1
        )

        self.assertEqual(link.label, 'Нашата Facebook страница')
        self.assertEqual(link.url, 'https://facebook.com/example')
        self.assertEqual(link.icon_class, 'fa-facebook')
        self.assertEqual(link.get_icon(), 'fa-facebook')
        self.assertEqual(str(link), 'Нашата Facebook страница (fa-facebook)')

    def test__social_link_creation_with_custom_icon(self):
        link = SocialLink.objects.create(
            label='TikTok профил',
            url='https://tiktok.com/@example',
            icon_class='custom',
            custom_icon='fa-tiktok',
            appearance_order=2
        )

        self.assertEqual(link.icon_class, 'custom')
        self.assertEqual(link.custom_icon, 'fa-tiktok')
        self.assertEqual(link.get_icon(), 'fa-tiktok')
        self.assertEqual(str(link), 'TikTok профил (fa-tiktok)')

    def test__default_appearance_order(self):
        link = SocialLink.objects.create(
            label='Уебсайт',
            url='https://example.com',
            icon_class='fa-globe'
        )

        self.assertEqual(link.appearance_order, 1)

    def test__icon_choices_are_valid(self):
        valid_choices = [choice[0] for choice in SocialLink.ICON_CHOICES]
        link = SocialLink.objects.create(
            label='Линк',
            url='https://example.com/link',
            icon_class='fa-link'
        )
        self.assertIn(link.icon_class, valid_choices)
