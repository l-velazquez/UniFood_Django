from django.shortcuts import render
from dotenv import load_dotenv
import os
import requests
from django.contrib import messages
import jwt

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



def set_favorite_place(request, id):
    token = request.session.get('jwt')
    token_data = jwt.decode(token, verify=False, algorithms=['HS256'], options={"verify_signature": False})
    token_user_email = token_data['email']

    headers = {
        'ApiKey': f'{api_key}',
        'Authorization': f'Bearer {token}',
    }
    
    get_user_by_email = requests.get(api_url + f'Users/email/{token_user_email}', headers=headers, verify=False)

    users_name = get_user_by_email.json()
    users_id = users_name['id']


    request_data = {
        'userId': users_id,
        'placeId': id
    }

    response = requests.post(api_url + 'FavoritePlaces', headers=headers, json=request_data, verify=False)

    if debug:
        print(f'URL: {api_url}FavoritePlaces')
        print(f'Status code: {response.status_code}')
        print(f'Response: {response.text}')

    