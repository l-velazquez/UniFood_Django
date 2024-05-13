from django.shortcuts import render
import requests
from dotenv import load_dotenv
import os
from django.contrib import messages

debug = os.getenv('DJANGO_DEBUG')

# Create your views here.

load_dotenv()
api_url = os.getenv('API_URL')

def get_all_universities(request):
    token = request.session.get('jwt')

    if not token:
        return render(request, 'login.html')
    
    # Get all universities from API
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(api_url + '/Universities/', headers=headers)

    if debug:
        print(f'URL: {api_url}/Universities/')
        print(f"Token: {token}")
        print(f'Status code: {response.status_code}')
        print(f'Response: {response.text}')
    if response.status_code == 401:
        messages.error(request, 'You are not authorized to view this page. Please login.')
        return render(request, 'login.html')
    
    elif response.status_code == 404:
        return render(request, 'error/404.html')

    universities = response
    return render(request, 'Universities.html', {'universities': universities})

def get_university(request, university_id):
    token = request.session.get('jwt')
    # Get all universities from API
    headers = {'Authorization': f'Bearer {token}'}

    # Get university from API
    response = requests.get(api_url + f'/universities/{university_id}/', headers=headers)   
    university = response.json()

    if debug:
        print(f'URL: {api_url}')
        print(f'Status code: {response.status_code}')
        print(f'Response: {response.text}')

    return render(request, 'university.html', {'university': university})
    