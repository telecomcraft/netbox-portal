import requests

from django.conf import settings
from django.test import TestCase

from .views import index


class ConnectionStatusTests(TestCase):

    def test_connection_status(self):
        url = f'{settings.NETBOX_URL}/api/status'
        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.SECRETS["NETBOX_TOKEN"]}',
        }

        # Suppress unsigned SSL error for local use
        response = requests.get(
            url,
            headers=headers,
            data=payload,
            verify=False
        )
        data = response.json()
        print(data)
        self.assertEquals(response.status_code, 200)


class ViewsTests(TestCase):

    def test_index(self):
        response = self.client.get('/')
        print(dir(response))
        self.assertEquals(response.status_code, 200)