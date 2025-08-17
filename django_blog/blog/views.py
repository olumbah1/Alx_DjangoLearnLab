from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import  UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CommentForm, CommentUpdateForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy # Import reverse_lazy to lazily resolve URLs, suitable for use in class-based views
from django.db.models import Q
# Create your Register views here.

# views.py - Debug version
def register_view(request):
    print(f"Request method: {request.method}")
    
    if request.method == 'POST':
        print("POST data received:", request.POST)
        
        form = UserRegisterForm(request.POST)
        print(f"Form created, is_valid: {form.is_valid()}")
        
        if form.is_valid():
            print("Form is valid, attempting to save...")
            try:
                user = form.save()
                print(f"User created successfully: {user.username}, ID: {user.id}")
                messages.success(request, f"Account created successfully for {user.username}! Please log in.")
                return redirect('login')
            except Exception as e:
                print(f"Error saving user: {str(e)}")
                messages.error(request, f"Error creating account: {str(e)}")
        else:
            print("Form is NOT valid")
            print("Form errors:", form.errors)
            print("Non-field errors:", form.non_field_errors())
            # Add error messages to display in template
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        print("GET request - creating empty form")
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
            return redirect('post-create') #Change to home page
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'blog/login.html')

#logout views

def logout_view(request):
    logout(request)
    return redirect('login')
        
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile

@login_required
def profile_view(request):
    # Ensure profile exists for the user
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    return render(request, 'blog/profile.html', {'u_form': u_form, 'p_form': p_form})

def profile_view(request):
    profile = request.user.profile  # or however you access it
    # pass profile in context
    context = {
        'profile': profile,
        # other context variables
    }
    return render(request, 'blog/profile.html', context)

# views.py
@login_required
def profile_update_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect('profile')  # Redirect back to profile view

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    return render(request, 'blog/profile_update.html', {
        'u_form': u_form,
        'p_form': p_form
    })


# Post Views classes with Authentication

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'   # Name for use in template (instead of default 'object_list')
    ordering = ['-published_date']      # Order results (latest first)
    paginate_by = 5                 # Optional: paginate results (5 per page)
    login_url = '/login/'           # Where to redirect if not logged in
    redirect_field_name = 'next'    # Keeps track of where to go after login
   
    
class PostDetailView(DetailView):
    model = Post   #means it fetches a post from the database.
    template_name = 'blog/post_detail.html' # Tells Django which HTML file to use.
    login_url = '/login/'           # Where to redirect if not logged in
    redirect_field_name = 'next'    # Keeps track of where to go after login
    
    def get_context_data(self, **kwargs): # Overrides the default method that prepares data for the template.
        context = super().get_context_data(**kwargs) # Starts by getting the default context (which includes post).
        # Get all comments for this post, ordered by newest first
        context['comments'] = Comment.objects.filter(post=self.object).order_by('-created_at') #Adds a list of all comments related to this post, ordered newest first.
        if self.request.user.is_authenticated: # This allows the user to submit a comment from the post detail page.
            context['comment_form'] = CommentForm() # empty form for posting new comment
        return context # Returns the updated context dictionary to be used by the template.
  
        
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    fields = ['title', 'content']
    login_url = '/login/'
    success_url = reverse_lazy('post-list')  # redirect here after successful create
    
    def form_valid(self, form):
        #Automatically set the login user as the author
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_update.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('post-list')
    login_url = '/login/'
    
    def form_valid(self, form):
        #Automatically set the login user as the author
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # Only author can edit
    
    
    # Delete a post (only by the author)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('post-list') #redirect after delete
    login_url = '/login/'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author # Only author can delete
    
#Comment Views for Post
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment  # The model that this view operates on
    form_class = CommentForm  # The form class to use for updating the comment
    template_name = 'blog/comment_create.html' 
    
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
        return redirect('post-detail', pk=pk) 
    
    
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # View for updating comments, only accessible to logged-in users who pass the test
    model = Comment  # The model that this view operates on
    form_class = CommentUpdateForm  # The form class to use for updating the comment
    template_name = 'blog/comment_update.html'  # The template that renders the comment update form
    
    def test_func(self):  # Custom permission logic to control who can update the comment
        comment = self.get_object()  # Get the comment instance being updated
        return self.request.user == comment.author  # Allow only the comment's author to update it
    
    def get_success_url(self):  # Define where to redirect after a successful update
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})  # Redirect to the detail view of the post related to the comment

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):  # View for deleting comments, restricted to logged-in users who pass the test
    model = Comment  # The model that this view operates on
    template_name = 'blog/comment_delete.html'  # The template that confirms deletion of the comment
    
    def test_func(self):  # Custom permission logic to control who can delete the comment
        comment = self.get_object()  # Get the comment instance being deleted
        return self.request.user == comment.author  # Allow only the comment's author to delete it
    
    def get_success_url(self):  # Define where to redirect after successful deletion
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})  # Redirect to the detail view of the post related to the comment


def search_posts(request):
    query = request.GET.get('q')   # Get the search query from URL
    results = []

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query) # Filter by title, content or tag
        ).distinct()                       # Avoid duplicate posts

    return render(request, 'blog/search_results.html', {'query': query, 'results': results})

def posts_by_tag(request, tag_name):    # Filter posts by tag name
    posts = Post.objects.filter(tags__name=tag_name)
    return render(request, 'blog/posts_by_tag.html', {'posts': posts, 'tag': tag_name})


class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/posts_by_tag.html'  # Make sure this template exists
    context_object_name = 'posts'

    def get_queryset(self):
        tag = self.kwargs.get('tag_slug')  # Get tag from URL
        return Post.objects.filter(tags__name__iexact=tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('tag_slug')  # Pass tag to template
        return context
