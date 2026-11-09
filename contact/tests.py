from django.test import TestCase
from django.urls import reverse


class ContactPageTests(TestCase):
    def test_shows_address_phone_email_and_map(self):
        response = self.client.get(reverse('contact'), secure=True)
        self.assertTemplateUsed(response, 'contact/contact.html')
        html = response.content.decode()
        page = html[:html.index('<footer')]  # the footer repeats the address
        for text in [
            '<h3>Contact Information</h3>',
            'Kim Lab',
            '456 Life Sciences Complex',
            '107 College Place',
            'Syracuse, NY 13244',
            'Office: (315) 443-8578',
            ">ekim112@syr.edu</span>",
            "copyToClipboard('contentToCopy2')",
            'src="/static/icons/copy_button.svg"',
            'src="https://www.google.com/maps/embed?',
        ]:
            self.assertIn(text, page)
