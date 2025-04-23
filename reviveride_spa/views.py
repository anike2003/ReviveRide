# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
# from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.mail import send_mail
from django.conf import settings
from .token import token_generator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse

# Local imports
from .models import Notification
from .token import token_generator



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
            return redirect('login') 

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
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(reverse('reset_password', kwargs={
                'uidb64': uid,
                'token': token
            }))

            send_mail(
                'Password Reset Link',
                f'Click the link to reset your password:\n{reset_url}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return render(request, 'Authentication_page/password_reset_done.html')
        else:
            error_message = "Email not found."
            return render(request, 'Authentication_page/forgotPassword.html', {'error_message': error_message})

    return render(request, 'Authentication_page/forgotPassword.html')


def Reset_password(request, uidb64, token):
    if request.method == 'POST':
        # Get new password and confirm password from POST data
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the passwords match
        if new_password != confirm_password:
            error_message = "Passwords do not match."
            return render(request, 'Authentication_page/resetPassword.html', {
                'error_message': error_message,
                'uidb64': uidb64,
                'token': token
            })

        try:
            # Decode the user ID
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)

            # Check if the token is valid
            if token_generator.check_token(user, token):
                # Set the new password and save the user
                user.set_password(new_password)
                user.save()

                # Optional: You can log the user in automatically after a successful reset.
                # Authenticate the user using the new password
                user = authenticate(request, username=user.username, password=new_password)
                if user is not None:
                    login(request, user)

                return render(request, 'Authentication_page/password_successful.html')
            else:
                error_message = "Token is invalid or expired."
                return render(request, 'Authentication_page/password_reset_confirm.html', {
                    'error_message': error_message,
                    'uidb64': uidb64,
                    'token': token
                })

        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            error_message = "User not found or invalid data."
            return render(request, 'Authentication_page/password_reset_confirm.html', {
                'error_message': error_message,
                'uidb64': uidb64,
                'token': token
            })

    # If GET request, show the reset password form
    return render(request, 'Authentication_page/resetPassword.html', {
        'uidb64': uidb64,
        'token': token
    })


def Dashboard(request):
    notifications = Notification.objects.filter(user=request.user)
    unread_count = notifications.filter(is_read=False).count()
    return render(request, 'dashboard.html',{'unread_count': unread_count})

def booking_view(request):
    if request.method == 'POST':
        Notification.objects.create(
            user=request.user,
            message='Your booking has been confirmed.',
            icon='📅'
        )
        return redirect('dashboard')

@login_required
def Notifications(request):
    search_query = request.GET.get('search', '')
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    if search_query:
        notifications = notifications.filter(
        title__icontains=search_query) | notifications.filter(
        message__icontains=search_query)
   
    return render(request, 'notification/notification.html', {
        'notifications': notifications,
        'unread_count': unread_count,
        'search_query': search_query
    })

@login_required
def notification_detail(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    if not notification.is_read:
        notification.is_read = True
        notification.save()
    return render(request, 'notification/notification_detail.html', {'notification': notification})

    
@login_required
@csrf_exempt
def mark_as_read(request, notification_id):
    if request.method == 'POST':
        notification = get_object_or_404(Notification, id=notification_id)
        notification.is_read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)

@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.delete()
    return redirect('notification')


@login_required
def create_notification(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        notification = Notification.objects.create(user=request.user, title=title, message=message)
        return redirect('notification')
    return render(request, 'notification/create_notification.html')

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

def Payment(request):
    return render(request, 'payment.html' )
