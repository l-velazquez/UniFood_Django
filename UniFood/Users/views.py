from django.shortcuts import render
from dotenv import load_dotenv
import os
import requests
from django.contrib import messages
import jwt 
from django.shortcuts import redirect
from django.core.paginator import Paginator

load_dotenv()

api_url = os.getenv('API_URL')
api_key = os.getenv('API_KEY')
debug = os.getenv('DJANGO_DEBUG')

# Create your views here.

def home(request):
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

    user= get_user_by_email.json()
    user_role = user['role']
    print(user_role)

    if user_role == 'Admin':
        return render(request, 'admin_home.html')
    

    extra_context = {'user': user}

    return render(request, 'home.html', extra_context)

def get_all_users(request):
    token = request.session.get('jwt')
    page = request.GET.get('page', 1)  # Get the current page number, default to 1
    page_size = request.GET.get('page_size', 10)  # Get the number of users per page, default to 10
    page_size = int(page_size)  # Ensure page_size is an integer

    if not token:
        return render(request, 'login.html')
    
    # Get all users from API with pagination
    headers = {
        'ApiKey': f'{api_key}',
        'Authorization': f'Bearer {token}',
    }

    response = requests.get(f'{api_url}Users?page={page}&pageSize={page_size}', headers=headers, verify=False)
    universities = requests.get(api_url + 'Universities', headers=headers, verify=False)
    universities = universities.json()
    
    if debug:
        print(f'URL: {api_url}Users?page={page}&pageSize={page_size}')
        print(f"Token: {token}")
        print(f'API Key: {api_key}')
        print(f'Status code: {response.status_code}')
    
    if response.status_code == 401:
        messages.error(request, 'You are not authorized to view this page. Please login.')
        return render(request, 'login.html')
    elif response.status_code == 404:
        return render(request, 'error/404.html')
    else:
        data = response.json()

        if isinstance(data, dict) and 'results' in data:
            users = data['results']  # Assuming the API response contains a 'results' field with the list of users
            total_users = data.get('total', len(users))  # Assuming the API response contains a 'total' field with the total number of users
        else:
            users = data  # If the API returns a list directly
            total_users = len(users)  # Total users is the length of the list

        paginator = Paginator(users, page_size)
        page_obj = paginator.get_page(page)

        extra_context = {'users': page_obj, 'page_obj': page_obj, 'total_users': total_users, 'page_size': page_size}

        if debug:
            print(f'Context: {extra_context}')

        return render(request, 'users.html', extra_context)
    

def profile(request):
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
    uni_id = user['universityId']
    uni_name = requests.get(api_url + f'Universities/{uni_id}', headers=headers, verify=False)
    university = uni_name.json()
    user_id = user['id']

    response = requests.get(api_url + f'Favorites/{user_id}', headers=headers, verify=False)
    response_data = response.json()

    favorite_places = []
    for favorite in response_data:
        place_id = favorite['placeId']
        get_places_from_favorites = requests.get(api_url + f'Places/{uni_id}?placeId={place_id}', headers=headers, verify=False)
        get_places_from_favorites_data = get_places_from_favorites.json()
        get_places_from_favorites_data['fav_id'] = favorite['id']
        favorite_places.append(get_places_from_favorites_data)
    
    if uni_name.status_code == 400:
        university = {'name': 'University not found'}

    elif uni_name.status_code == 401:
        messages.error(request, 'You are not authorized to view this page. Please login.')
        return render(request, 'login.html')
    
    
    extra_context = {'user': user, 'university': university, 'favorite_places': favorite_places}

    
    return render(request, 'profile.html', extra_context)

def edit_profile(request):
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
    uni_id = user['universityId']
    user_uni = requests.get(api_url + f'Universities/{uni_id}', headers=headers, verify=False)
    user_uni = user_uni.json()
    all_uni = requests.get(api_url + 'Universities', headers=headers, verify=False)
    universities = all_uni.json()

    extra_context = {'user': user, 'user_uni': user_uni, 'universities': universities}

    if debug:
        print(f'Context: {extra_context}')


    if request.method == 'POST':
        new_email = request.POST.get('email')
        new_first_name = request.POST.get('first_name')
        new_last_name = request.POST.get('last_name')
        new_password = request.POST.get('password')
        new_university_id = request.POST.get('university_id')
        new_data = {
            'email': new_email,
            'firstName': new_first_name,
            'lastName': new_last_name,
            'password': new_password,
            'universityId': new_university_id
        }
        response = requests.put(api_url + 'Users', json=new_data, headers=headers, verify=False)

        if response.status_code == 200:
            messages.success(request, 'Profile updated successfully')
            return redirect('/profile')
        else:
            messages.error(request, 'Profile update failed')
            return render(request, 'edit.html')

    return render(request, 'edit.html', extra_context)


def admin_users(request):
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
    user_role = user['role']
    if user_role != 'Admin':
        return render(request, 'error/403.html')
    
    extra_context = {'user': user}

    return render(request, 'admin_home.html', extra_context)
    