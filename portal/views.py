import requests

from django.conf import settings
from django.shortcuts import render, HttpResponse


def index(request):
    url = 'https://192.168.1.7/api/status'
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {settings.SECRETS["NETBOX_TOKEN"]}',
    }

    # Suppress unsigned SSL error for local use
    response = requests.get(url, headers=headers, data=payload, verify=False)
    data = response.json()

    # TODO: Compare to latest release on GitHub?
    #print(data)
    return HttpResponse(data['netbox-version'])
