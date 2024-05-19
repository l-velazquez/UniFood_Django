from django.shortcuts import render
import requests
from dotenv import load_dotenv
import os
from django.contrib import messages

debug = os.getenv('DJANGO_DEBUG')

# Create your views here.

load_dotenv()
api_url = os.getenv('API_URL')
api_key = os.getenv('API_KEY')

def get_all_universities(request):
    token = request.session.get('jwt')

    # if not token:
    #     return render(request, 'login.html')
    
    # Get all universities from API
    headers = {
        'ApiKey': f'{api_key}',
        'Authorization': f'Bearer {token}',
    }

    response = requests.get(api_url + 'Universities', headers=headers, verify=False)

    # if debug:
    #     print(f'URL: {api_url}Universities')
    #     # print(f"Token: {token}")
    #     # print(f'API Key: {api_key}')
    #     # print(f'Status code: {response.status_code}')
    #     # print(f'Headers: {headers}')
    #     # print(f'Response: {response.text}')

    if response.status_code == 401:
        messages.error(request, 'You are not authorized to view this page. Please login.')
        return render(request, 'login.html')
    
    elif response.status_code == 404:
        return render(request, 'error/404.html')

    universities = response.json()

    extra_context = {'universities': universities}

    # if debug:
    #     print(f'Context: {extra_context}')
    # print(universities_name)

    return render(request, 'Universities.html', extra_context)

def get_university(request, university_id):
    token = request.session.get('jwt')
    # Get all universities from API
    headers = {'Authorization': f'Bearer {token}'}

    # Get university from API
    response = requests.get(api_url + f'/universities/{university_id}/', headers=headers)   
    university = response.json()

    # if debug:
    #     print(f'URL: {api_url}')
    #     print(f'Status code: {response.status_code}')
    #     print(f'Response: {response.text}')

    return render(request, 'university.html', {'university': university})
    