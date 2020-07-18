from django.urls import reverse
from django.test import TestCase
from django.test import Client


class UrlsAvailabilityTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_public_url(self):
        urls = [
            (reverse('index'), 'Welcome to Test Program'),
        ]
        for url, content in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            if not content:
                self.assertContains(response.content.decode(), content)

    def test_private_urls(self):
        private_urls = [
            reverse('test:leader_list'),
            reverse('test:test_list'),
        ]
        for url in private_urls:
            response = self.client.get(url)
            self.assertRedirects(response, '{}?next={}'.format(reverse('account:login'), url))
