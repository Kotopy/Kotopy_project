from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return/<int:book_id>/', views.return_book, name='return_book'),
    path('my-library/', views.my_library, name='my_library'),
    path('search/', views.search_books, name='search_books'),
     path('details/<int:id>/', views.book_details, name='book_details'),
     path('books/', views.book_list, name='book_list'),
]
