from django.test import TestCase
from django.urls import reverse


class OpportunityPageTests(TestCase):
    def test_lists_open_positions_and_how_to_apply(self):
        response = self.client.get(reverse('opportunity'), secure=True)
        self.assertTemplateUsed(response, 'opportunity/opportunity.html')
        for text in [
            '<h3>Available Positions</h3>',
            '<li>Postdoctoral Fellow</li>',
            '<li>Graduate Student</li>',
            '<li>Lab Technician</li>',
            '<li>Undergraduate Student</li>',
            '<li>your CV</li>',
            '<li>contact information for three references</li>',
            '"[POSITION] - your name"',
            "copyToClipboard('contentToCopy1')",
            'src="/static/icons/copy_button.svg"',
        ]:
            self.assertContains(response, text)
