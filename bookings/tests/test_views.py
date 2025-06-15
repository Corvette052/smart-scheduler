from django.urls import reverse
from django.test import TestCase


class ThankYouViewTests(TestCase):
    def test_thank_you_page(self):
        response = self.client.get(reverse('thank_you'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Thank You")
