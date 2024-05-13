from django.shortcuts import render
import requests
from dotenv import load_dotenv
import os

load_dotenv()
debug = os.getenv('DJANGO_DEBUG')

api_url = os.getenv('API_URL')

# Create your views here.

def get_menus(id,request):
    token = request.session.get('jwt')
    if not token:
        return render(request, 'login.html')
    
    # Get all menus from API
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(api_url + f'/menus/{id}/', headers=headers)

    if debug:
        print(f'URL: {api_url}')
        print(f'Status code: {response.status_code}')
        print(f'Response: {response.text}')
    
    menus = response.json()

    return menus

    