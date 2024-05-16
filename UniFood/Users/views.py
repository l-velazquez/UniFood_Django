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

def home(request):
    token = request.session.get('jwt')
    token_data = jwt.decode(token, verify=False, algorithms=['HS256'], options={"verify_signature": False})
    token_user_email = token_data['email']

    headers = {
        'ApiKey': f'{api_key}',
        'Authorization': f'Bearer {token}',
    }

    if debug:
        print(f'URL: {api_url}Users/email/{token_user_email}')
        print(f"Token: {token}")
        print(f'API Key: {api_key}')

    get_user_by_email = requests.get(api_url + f'Users/email/{token_user_email}', headers=headers, verify=False)

    if debug:
        print(f'Status code: {get_user_by_email.status_code}')
        print(f'Response: {get_user_by_email.text}')

    users_name = get_user_by_email.json()
    users_name = users_name['firstName']

    extra_context = {'users_name': users_name}

    if not token:
        return render(request, 'login.html')
    return render(request, 'home.html', extra_context)

def get_all_users(request):
    token = request.session.get('jwt')

    if not token:
        return render(request, 'login.html')
    
    # Get all users from API
    headers = {
        'ApiKey': f'{api_key}',
        'Authorization': f'Bearer {token}',
    }

    response = requests.get(api_url + 'Users', headers=headers, verify=False)

    if debug:
        print(f'URL: {api_url}Users')
        print(f"Token: {token}")
        print(f'API Key: {api_key}')
        print(f'Status code: {response.status_code}')
    
    if response.status_code == 401:
        messages.error(request, 'You are not authorized to view this page. Please login.')
        return render(request, 'login.html')
    elif response.status_code == 404:
        return render(request, 'error/404.html')
    else:
        users = response.json()

        extra_context = {'users': users}

        if debug:
            print(f'Context: {extra_context}')

        return render(request, 'Users.html', extra_context)