from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book # Replace with Book if you renamed it
from .forms import ExampleForm # ✅ import the form, not 'query'
# Create your views here.

# Only users with 'can_view' permission can access this view
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()  
    return render(request, 'bookshelf/book_list.html', {'books': books})


# views.py

def search_view(request):
    form = ExampleForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['q']
        results = Book.objects.filter(title__icontains=query)
    else:
        results = Book.objects.none()
    return render(request, 'form_example.html', {'results': results})

# views.py
from django.shortcuts import render
from .forms import ExampleForm
from .models import Book  # assuming you have a Book model

def example_books(request):
    form = ExampleForm(request.GET or None)
    results = []
    if form.is_valid():
        query = form.cleaned_data['q']
        results = Book.objects.filter(title__icontains=query) if query else Book.objects.all()
    return render(request, 'form_example.html', {'form': form, 'results': results})
