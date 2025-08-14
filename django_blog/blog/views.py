from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import  UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# Create your Register views here.
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
    else: 
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

# login views
def login_view(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') #Change to home page
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

#logout views

def logout_view(request):
    logout(request)
    return redirect('login')
        
@login_required #Prevents non-logged-in users from accessing the profile page.
def profile_view(request):
    if request.method =='POST': # This means the user submitted the profile edit form.
        u_form = UserUpdateForm(request.POST, instance=request.user) # Tells the form to update the current logged-in user instead of creating a new one.
        p_form = ProfileUpdateForm(request.POST, request.FILES) #Handles profile picture uploads.
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated!") # Stores a success message to display on the page after saving.
            return redirect('profile') #Reloads the page to show updated info after form submission.
    else:                               #Loads the form pre-filled with the current user’s details.
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'profile.html', {'u_form': u_form, 'p_form':p_form})