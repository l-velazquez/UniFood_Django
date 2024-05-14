from django.shortcuts import render
import requests
from dotenv import load_dotenv
import os
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.

load_dotenv()
debug = os.getenv('DJANGO_DEBUG')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # For debugging purposes
          # Set to False in production
        if debug:
            print(f'Email: {email}')
            print(f'Password: {password}')

        # Send credentials to API
        api_url = os.getenv('API_URL') + 'Login'

        data = {
            'email': email,
            'password': password
        }
        headers = {
            'Content-Type': 'application/json',
            'ApiKey': os.getenv('API_KEY')
        }
        response = requests.post(api_url, json=data, headers=headers, verify=False)

        if debug:
            print(f'URL: {api_url}')
            print(f'Status code: {response.status_code}')
            print(f'Response: {response.text}')  # Changed to print the text of the response
        
        #save the response JWT to django session
        token = response.text
        request.session['jwt'] = token

        if response.status_code == 200:
            # Successful login
            messages.success(request, 'You have successfully logged in')
            return redirect("/home")
        elif response.status_code == 400:
            messages.error(request, 'Invalid email or password')
            return render(request, 'login.html')
        elif response.status_code == 401:
            messages.error(request, 'Unauthorized')
            return render(request, 'error/401.html')
        elif response.status_code == 404:
            return render(request, 'error/404.html')
        else:
            # Failed login
            return render(request, 'failure.html')
    
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        university_id = request.POST.get('university_id')

        data = {
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'university_id': university_id
        }
        headers = {
            'Content-Type': 'application/json',
            'ApiKey': os.getenv('API_KEY')
        }

        api_url = os.getenv('API_URL') + 'Register'

        response = requests.post(api_url, json=data, headers=headers, verify=False)

        if debug:
            print(f'URL: {api_url}')
            print(f'Status code: {response.status_code}')
            print(f'Headers: {headers}')
            print(f'Response: {response.text}')
        
        if response.status_code == 200:
            messages.success(request, 'You have successfully registered')
            return redirect('/login')
        elif response.status_code == 400:
            messages.error(request, 'Invalid email or password')
            return render(request, 'register.html')
        elif response.status_code == 401:
            messages.error(request, 'Unauthorized')
            return render(request, 'error/401.html')
        elif response.status_code == 404:
            return render(request, 'error/404.html')
        else:
            return render(request, 'failure.html')
    return render(request, 'register.html')

