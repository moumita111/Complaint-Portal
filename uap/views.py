from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Login view
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.email.endswith('@uap-bd.edu'):
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Only Students with UAP Mail can login.')
                return redirect('login')  
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')  
    return render(request, 'login.html')




# Register view
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')  

        if not email.endswith('@uap-bd.edu'):
            messages.error(request, 'Only Students with UAP Mail can register.')
            return redirect('register')  

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')  
        except ValidationError as e:
            messages.error(request, f'Error: {e.message}')
            return redirect('register') 
        except Exception as e:
            messages.error(request, 'An error occurred during registration.')
            return redirect('register')  

    return render(request, 'register.html')


