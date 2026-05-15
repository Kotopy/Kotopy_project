from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Book, BorrowedBook
import os

def is_admin(user):
    return user.is_authenticated and (
        user.is_staff or
        user.groups.filter(name='admin').exists() or
        hasattr(user, 'profile') and user.profile.role == 'admin'
    )

admin_required = user_passes_test(is_admin, login_url='/auth/login/')


@login_required
@admin_required
def admin_dashboard(request):
    books = Book.objects.all().order_by('title')
    total_books = books.count()
    total_copies = sum(b.copies for b in books)
    total_borrowed = BorrowedBook.objects.count()
    out_of_stock = books.filter(copies=0).count()

    category = request.GET.get('category', '')
    search = request.GET.get('search', '')
    if category:
        books = books.filter(category=category)
    if search:
        books = books.filter(title__icontains=search) | books.filter(author__icontains=search)

    return render(request, 'books/admin_dashboard.html', {
        'books': books,
        'total_books': total_books,
        'total_copies': total_copies,
        'total_borrowed': total_borrowed,
        'out_of_stock': out_of_stock,
        'categories': Book.CATEGORY_CHOICES,
        'selected_category': category,
        'search': search,
    })


@login_required
@admin_required
@login_required
@admin_required
def admin_add_book(request):
    if request.method == 'POST':
        try:
            book = Book(
                code=request.POST['code'],
                title=request.POST['title'],
                author=request.POST['author'],
                category=request.POST['category'],
                year=int(request.POST['year']),
                copies=int(request.POST['copies']),
                description=request.POST['description'],
            )
            if 'image' in request.FILES:
                book.image = request.FILES['image']
            book.save()
            messages.success(request, f'"{book.title}" added successfully!')
            return redirect('admin_dashboard')
        except Exception as e:
            messages.error(request, f'Error: {e}')
    return render(request, 'books/admin_book_form.html', {
        'action': 'Add',
        'categories': Book.CATEGORY_CHOICES,
    })


@login_required
@admin_required
def admin_edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        try:
            book.code = request.POST['code']
            book.title = request.POST['title']
            book.author = request.POST['author']
            book.category = request.POST['category']
            book.year = int(request.POST['year'])
            book.copies = int(request.POST['copies'])
            book.description = request.POST['description']
            if 'image' in request.FILES:
                book.image = request.FILES['image']
            book.save()
            messages.success(request, f'"{book.title}" updated successfully!')
            return redirect('admin_dashboard')
        except Exception as e:
            messages.error(request, f'Error: {e}')
    return render(request, 'books/admin_book_form.html', {
        'action': 'Edit',
        'book': book,
        'categories': Book.CATEGORY_CHOICES,
    })


@login_required
@admin_required
def admin_delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'"{title}" deleted successfully!')
        return redirect('admin_dashboard')
    return render(request, 'books/admin_confirm_delete.html', {'book': book})
