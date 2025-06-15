from django.test import TestCase
from django.urls import reverse


class ThankYouViewTests(TestCase):
    def test_thank_you_view_renders_template(self):
        url = reverse('thank_you')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/thank_you.html')
