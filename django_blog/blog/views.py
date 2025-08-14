from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import  UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

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
    return render(request, 'blog/register.html', {'form': form})

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
    return render(request, 'blog/login.html')

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
    return render(request, 'blog/profile.html', {'u_form': u_form, 'p_form':p_form})

# Post Views classes with Authentication

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'   # Name for use in template (instead of default 'object_list')
    ordering = ['-created_at']      # Order results (latest first)
    paginate_by = 5                 # Optional: paginate results (5 per page)
    login_url = '/login/'           # Where to redirect if not logged in
    redirect_field_name = 'next'    # Keeps track of where to go after login
   
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    login_url = '/login/'           # Where to redirect if not logged in
    redirect_field_name = 'next'    # Keeps track of where to go after login
    
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = ['title', 'content']
    login_url = '/login/'
    
    def form_valid(self, form):
        #Automatically set the login user as the author
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # Only author can edit
    
    
    # Delete a post (only by the author)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post-delete.html'
    success_url = reverse_lazy('post-list') #redirect after delete
    login_url = '/login/'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author