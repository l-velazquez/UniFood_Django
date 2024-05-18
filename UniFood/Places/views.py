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



def set_favorite(request, id):
    token = request.session.get('jwt')
    if not token:
        return render(request, 'login.html')
    
    token_data = jwt.decode(token, verify=False, algorithms=['HS256'], options={"verify_signature": False})
    token_user_email = token_data['email']

    headers = {
        'ApiKey': f'{api_key}',
        'Authorization': f'Bearer {token}',
    }
    
    get_user_by_email = requests.get(api_url + f'Users/email/{token_user_email}', headers=headers, verify=False)

    users_name = get_user_by_email.json()
    users_id = users_name['id']
    university_id_of_user = users_name['universityId']


    request_data = {
        'userId': users_id,
        'placeId': id
    }

    print(request_data)
    response = requests.post(api_url + 'Favorites', headers=headers, json=request_data, verify=False)

    if debug:
        print(f'URL: {api_url}FavoritePlaces')
        print(f'Status code: {response.status_code}')
        print(f'Response: {response.text}')

    if response.status_code == 401:
        messages.error(request, 'You are not authorized to view this page. Please login.')
        return render(request, 'login.html')
    elif response.status_code == 404:
        return render(request, 'error/404.html')
    else:
        messages.success(request, 'Place added to favorites!')
        return view_favorite(request)
    

def view_favorite(request):
    token = request.session.get('jwt')
    if not token:
        return render(request, 'login.html')
    
    token_data = jwt.decode(token, verify=False, algorithms=['HS256'], options={"verify_signature": False})
    token_user_email = token_data['email']

    headers = {
        'ApiKey': f'{api_key}',
        'Authorization': f'Bearer {token}',
    }
    
    get_user_by_email = requests.get(api_url + f'Users/email/{token_user_email}', headers=headers, verify=False)

    user = get_user_by_email.json()
    user_id = user['id']
    users_university_id = user['universityId']

    # get university name from user
    university = requests.get(api_url + f'Universities/{users_university_id}', headers=headers, verify=False)
    university = university.json()


    # get all favorite places from user
    response = requests.get(api_url + f'Favorites/{user_id}', headers=headers, verify=False)
    response_data = response.json()

    favorite_places = []
    for favorite in response_data:
        place_id = favorite['placeId']
        get_places_from_favorites = requests.get(api_url + f'Places/{users_university_id}?placeId={place_id}', headers=headers, verify=False)
        get_places_from_favorites_data = get_places_from_favorites.json()
        get_places_from_favorites_data['fav_id'] = favorite['id']
        favorite_places.append(get_places_from_favorites_data)

    # get all places from users university
    get_all_places = requests.get(api_url + f'Places/{users_university_id}', headers=headers, verify=False)
    all_places = get_all_places.json()

    # Remove favorite places from all places
    favorite_place_ids = {fav['id'] for fav in favorite_places}
    places = [place for place in all_places if place['id'] not in favorite_place_ids]

    if response.status_code == 401:
        messages.error(request, 'You are not authorized to view this page. Please login.')
        return render(request, 'login.html')
    elif response.status_code == 404:
        return render(request, 'error/404.html')
    else:
        extra_context = {'favorite_places': favorite_places, 'places': places, 'user': user, 'university': university}

    return render(request, 'Favorites.html', extra_context)


def remove_favorite(request, id):
    token = request.session.get('jwt')
    if not token:
        return render(request, 'login.html')
    
    token_data = jwt.decode(token, verify=False, algorithms=['HS256'], options={"verify_signature": False})
    token_user_email = token_data['email']

    headers = {
        'ApiKey': f'{api_key}',
        'Authorization': f'Bearer {token}',
    }
    
    get_user_by_email = requests.get(api_url + f'Users/email/{token_user_email}', headers=headers, verify=False)

    users_name = get_user_by_email.json()
    users_id = users_name['id']

    response = requests.delete(api_url + f'Favorites/{id}', headers=headers, verify=False)

    if debug:
        print(f'URL: {api_url}Favorites/{users_id}/{id}')
        print(f'Status code: {response.status_code}')
        print(f'Response: {response.text}')

    if response.status_code == 401:
        messages.error(request, 'You are not authorized to view this page. Please login.')
        return render(request, 'login.html')
    elif response.status_code == 404:
        return render(request, 'error/404.html')
    else:
        messages.success(request, 'Place removed from favorites!')
        return view_favorite(request)