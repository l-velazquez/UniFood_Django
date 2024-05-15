from django.shortcuts import render
from dotenv import load_dotenv
import os
import requests
from django.contrib import messages

load_dotenv()

api_url = os.getenv('API_URL')
api_key = os.getenv('API_KEY')
debug = os.getenv('DJANGO_DEBUG')

# Create your views here.
def get_all_places(request, id):
    token = request.session.get('jwt')

    if not token:
        return render(request, 'login.html')
    
    extra_context = {}
     # Get all places from API
    headers = {
            'ApiKey': f'{api_key}',
            'Authorization': f'Bearer {token}',
    }
    response = requests.get(api_url + f'Places/{id}', headers=headers, verify=False)
    get_university = requests.get(api_url + f'Universities/{id}', headers=headers, verify=False)
    places = response.json()
    university = get_university.json()
    
    if debug:
        print(f'URL: {api_url}Places/{id}')
        print(f'Status code: {response.status_code}')
        print(f'Headers: {headers}')
        print(f'Response: {response.text}')

    if response.status_code == 401:
        messages.error(request, 'You are not authorized to view this page. Please login.')
        return render(request, 'login.html')
    elif response.status_code == 404:
        return render(request, 'error/404.html')
    else:
        extra_context = {'places': places, 'university': university}

    
    return render(request, 'Places.html', extra_context)