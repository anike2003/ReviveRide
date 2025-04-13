from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib import messages



def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()   
        password = request.POST.get('password')  

      
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        else:
            
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user) 
            messages.success(request, "Signup successful! Welcome!")
            return redirect('dashboard') 

    return render(request, 'Authentication_page/signup.html') 



def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip() 
        password = request.POST.get('password') 
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user) 
            return redirect('dashboard')  
        else:
            messages.error(request, "Incorrect username or password.")
    return render(request, 'Authentication_page/login.html')


def Logout(request):
    logout(request)  
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


def Create_new_password(request):
     
    return render(request, 'Authentication_page/create_new_password.html' )

def Password_successful(request):
    return render(request, 'Authentication_page/password_successful.html' )

def Forgot_password(request):
    return render(request, 'Authentication_page/forgotPassword.html' )

def Dashboard(request):
    return render(request, 'dashboard.html' )

def CreateID(request):
    return render(request, 'createID.html' )

def Feedback(request):
    return render(request, 'feedback.html' )

def Chatbox(request):
    return render(request, 'chatbox.html' )

def LocationFinder(request):
    return render(request, 'locationFinder.html' )

def Service(request):
    return render(request, 'service.html' )

def Notification(request):
    return render(request, 'notification.html' )

def Payment(request):
    return render(request, 'payment.html' )
