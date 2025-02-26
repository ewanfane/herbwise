# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required

# In your views.py
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Pass request
        if form.is_valid():
            user = form.get_user()  # Get the authenticated User object
            login(request, user)
            return redirect('home')  # Or your success URL
    else:
        form = AuthenticationForm()
    return render(request, 'users/register.html', {'form': form, 'template_type': 'login'})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log them in immediately
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form, 'template_type': 'register'})
 
def change_password_view(request):
     if request.method == 'POST':
         form = PasswordChangeForm(request.user, request.POST) # Pass the current user
         if form.is_valid():
             user = form.save()
             # update_session_auth_hash(request, user) # Important for password changes! Prevents being logged out
             login(request, user) # log them back in since password changed
             return redirect('password_change_done')  # Redirect after success
     else:
         form = PasswordChangeForm(request.user)
     return render(request, 'change_password.html', {'form': form})
 
 
def logout_view(request):
    logout(request)
    return redirect('login')