from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Notification
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt






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
    return render(request, 'Authentication_page/forgotPassword.html' )
@login_required
def Dashboard(request):
    notifications = Notification.objects.filter(user=request.user)
    unread_count = notifications.filter(is_read=False).count()
    return render(request, 'dashboard.html',{'unread_count': unread_count})

def booking_view(request):
    if request.method == 'POST':
        # Handle the booking logic
        Notification.objects.create(
            user=request.user,
            message='Your booking has been confirmed.',
            icon='📅'
        )
        return redirect('dashboard')

@login_required
def Notifications(request):
    # Fetch all notifications for the current user, ordered by created_at
    search_query = request.GET.get('search', '')
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Count the number of unread notifications
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
# def mark_as_read(request, notification_id):
#     notification = get_object_or_404(Notification, id=notification_id)
#     notification.is_read = True
#     notification.save()
#     return redirect('notification')

# @login_required
# def delete_notification(request, notification_id):
#     try:
#         notification = get_object_or_404(Notification, id=notification_id, user=request.user)
#     except Http404:
#         print(f"Notification with ID {notification_id} does not exist for user {request.user.id}.")
#         raise  # Re-raise the exception after logging
#     if request.method == 'POST':
#         # notification = Notification.objects.get(id=notification_id)
#         notification.delete()
#         return redirect('notification')
#     return render(request, 'notification/delete_notification.html', {'notification': notification})
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

# def Notification(request):
#     return render(request, 'notification.html' )

def Payment(request):
    return render(request, 'payment.html' )
