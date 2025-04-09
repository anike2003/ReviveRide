from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account created for {email}! You can now log in.')
            login(request, user)  # Automatically log in the user after signup
            return redirect('login.html')  # Redirect to the dashboard after signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Login view
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email= email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard.html')  # Redirect to the dashboard after login
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'login.html')  # Render your existing login template



def Dashboard(request):
    return render(request, 'dashboard.html' )

def Create_new_password(request):
     
    return render(request, 'create_new_password.html' )

def Password_successful(request):
    return render(request, 'password_successful.html' )