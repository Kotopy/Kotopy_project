from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book, BorrowedBook
from django.shortcuts import render, get_object_or_404
from .models import Book


def book_list(request):
    """Display all available books with optional category filter."""
    category = request.GET.get('category', '')
    books = Book.objects.all()

    if category:
        books = books.filter(category=category)

    # Get borrowed book IDs for the current user (to show borrow/return button)
    borrowed_ids = []
    if request.user.is_authenticated:
        borrowed_ids = BorrowedBook.objects.filter(
            user=request.user
        ).values_list('book_id', flat=True)

    categories = Book.CATEGORY_CHOICES

    return render(request, 'books/book_list.html', {
        'books': books,
        'borrowed_ids': borrowed_ids,
        'categories': categories,
        'selected_category': category,
        'page': 'books',
    })


@login_required
def borrow_book(request, book_id):
    """Borrow a book if copies are available and not already borrowed."""
    book = get_object_or_404(Book, id=book_id)

    already_borrowed = BorrowedBook.objects.filter(
        user=request.user, book=book
    ).exists()

    if already_borrowed:
        messages.warning(request, f'You already borrowed "{book.title}".')
    elif book.copies <= 0:
        messages.error(request, f'Sorry, "{book.title}" is currently out of stock.')
    else:
        BorrowedBook.objects.create(user=request.user, book=book)
        book.copies -= 1
        book.save()
        messages.success(request, f'"{book.title}" has been added to your library!')

    return redirect(request.META.get('HTTP_REFERER', 'book_list'))


@login_required
def return_book(request, book_id):
    """Return a borrowed book."""
    book = get_object_or_404(Book, id=book_id)
    borrowed = BorrowedBook.objects.filter(user=request.user, book=book).first()

    if borrowed:
        borrowed.delete()
        book.copies += 1
        book.save()
        messages.success(request, f'"{book.title}" has been returned successfully.')
    else:
        messages.error(request, 'You have not borrowed this book.')

    return redirect(request.META.get('HTTP_REFERER', 'my_library'))


@login_required
def my_library(request):
    """Show all books borrowed by the current user."""
    borrowed_books = BorrowedBook.objects.filter(
        user=request.user
    ).select_related('book').order_by('-borrow_date')

    return render(request, 'books/my_library.html', {
        'borrowed_books': borrowed_books,
        'page': 'my_library',
    })

def search_books(request):
    title = request.GET.get('title', '').strip()
    author = request.GET.get('author', '').strip()
    category = request.GET.get('category', '').strip()
    year = request.GET.get('year', '').strip()

    results = None

    if any([title, author, category, year]):
        results = Book.objects.all()
        if title:
            results = results.filter(title__icontains=title)
        if author:
            results = results.filter(author__icontains=author)
        if category:
            results = results.filter(category=category)
        if year:
            results = results.filter(year=year)

    borrowed_ids = []
    if request.user.is_authenticated:
        borrowed_ids = BorrowedBook.objects.filter(
            user=request.user
        ).values_list('book_id', flat=True)

    return render(request, 'books/search.html', {
        'results': results,
        'title': title,
        'author': author,
        'category': category,
        'year': year,
        'categories': Book.CATEGORY_CHOICES,
        'borrowed_ids': borrowed_ids,
    })



def book_details(request, id):
    book = get_object_or_404(Book, id=id)

    suggested_books = Book.objects.exclude(id=id)[:6]

    return render(request, 'books/book_details.html', {
        'book': book,
        'suggested_books': suggested_books
    })