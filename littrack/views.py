from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django import forms
from django.contrib import messages
from django.db.models import Count
from .models import Book
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .helpers import dump
from .forms import RegisterForm, SearchBookForm, EditBookForm


def index(request):
    highest_rated_books = Book.objects.all().values('isbn13', 'title', 'cover', 'authors', 'rating').annotate(read_count=Count('rating')).order_by('-rating')[:5]
    most_recent_books = Book.objects.all().order_by('-created_at')[:5]
    most_read_books = Book.objects.all().values('isbn13', 'title', 'cover', 'authors', 'rating').annotate(read_count=Count('isbn13')).order_by('-read_count')[:5]

    context = {
        'title': 'Dashboard',
        'highest_rated_books': highest_rated_books,
        'most_recent_books': most_recent_books,
        'most_read_books': most_read_books
    }

    return render(request, 'littrack/index.html', context)

def my_books(request):
    books = Book.objects.filter(reader=request.user.id).order_by('-created_at')

    context = {
        'title': 'My Books',
        'books': books
    }

    return render(request, 'littrack/my-books.html', context)

def edit_book(request):
    book_id = request.path.split('/')[3]
    book = Book.objects.get(id=book_id, reader=request.user.id)

    if request.method == 'POST':
        form = EditBookForm(request.POST)

        if form.is_valid():
            book.title = form.cleaned_data['title']
            book.authors = form.cleaned_data['authors']
            book.isbn13 = form.cleaned_data['isbn13']
            book.cover = form.cleaned_data['cover']
            book.rating = form.cleaned_data['rating']
            book.save()
            messages.success(request, 'Your book has been updated.')

    else:
        form = EditBookForm(initial={
            'title': book.title,
            'authors': book.authors,
            'isbn13': book.isbn13,
            'cover': book.cover,
            'rating': book.rating
        })

    context = {
        'title': 'Edit',
        'form': form,
        'book': book
    }

    return render(request, 'littrack/edit-book.html', context)

def delete_book(request):
    book_id = request.path.split('/')[4]
    Book.objects.filter(id=book_id, reader=request.user.id).delete()

    messages.success(request, 'Your book has been deleted.')
    
    return HttpResponseRedirect('/books/')

def add_book(request):
    if request.method == 'POST':
        data = request.POST

        b = Book(cover=data['cover'], title=data['title'], authors=data['authors'], isbn13=data['isbn13'], reader=request.user)
        b.save()
        return JsonResponse({ 'status': 200 })

    else:
        books = Book.objects.all()
        form = SearchBookForm()

        context = {
            'title': 'Add a Book',
            'form': form,
            'books': books
        }

        return render(request, 'littrack/add-book.html', context)

# def isbndb_proxy(request):
#     url = request.GET['url']

#     return JsonResponse({ 'hello': url })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            first = form.cleaned_data['first']
            last = form.cleaned_data['last']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(email, email, password)
            user.first_name = first
            user.last_name = last
            user.save()

            authenticate(username=email, password=password)

            return HttpResponseRedirect('/')

    else:
        form = RegisterForm()

    context = {
        'title': 'Welcome to LitTrack!',
        'form': form
    }

    return render(request, 'registration/register.html', context)
