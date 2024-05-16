"""
URL configuration for UniFood project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Authentication import views as auth_views
from Universities import views as uni_views
from Places import views as place_views
from Menus import views as menu_views
from Users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('register/', auth_views.register, name='register'),
    path('home/', user_views.home, name='home'),
    path('universities/', uni_views.get_all_universities, name='universities'),
    path('universities/<int:university_id>/', uni_views.get_university, name='university'),
    path('places/<int:id>', place_views.get_all_places, name='places'),
    #path('menus/', menu_views.get_all_menus, name='menus'),
    path('menus/<int:id>/<int:university_id>/', menu_views.get_menus, name='menu'),
    path('profile/', user_views.profile, name='profile'),

]
