from django.shortcuts import render
import requests
from dotenv import load_dotenv
import os
from django.contrib import messages


load_dotenv()
debug = os.getenv('DJANGO_DEBUG')

api_url = os.getenv('API_URL')

def get_menus(request, id, university_id):
    token = request.session.get('jwt')
    if not token:
        return render(request, 'login.html')
    headers = {'Authorization': f'Bearer {token}',
               'ApiKey': os.getenv('API_KEY')
               } 

    # Get all menus from API
    response = requests.get(api_url + f'menus/{id}/', headers=headers, verify=False)
    place_name = requests.get(api_url + f'places/{university_id}?placeId={id}', headers=headers, verify=False)
    place = place_name.json()

    # if debug:
    #     print(f'URL: {api_url}menus/{id}/')
    #     print(f'Status code: {response.status_code}')
    #     print(f'Response: {response.text}')
    
    menus = response.json()
    if response.status_code == 401:
        messages.error(request, 'You are not authorized to view this page. Please login.')
        return render(request, 'login.html')
    elif response.status_code == 404:
        return render(request, 'error/404.html')
    else:
        extra_context = {'menus': menus, 'place': place}

        # if debug:
        #     print(f'Context: {extra_context}')

    return render(request, 'Menu.html', extra_context)


