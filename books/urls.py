from django.urls import path
from . import views, admin_views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return/<int:book_id>/', views.return_book, name='return_book'),
    path('my-library/', views.my_library, name='my_library'),
    path('search/', views.search_books, name='search_books'),
    path('details/<int:id>/', views.book_details, name='book_details'),

    # Admin panel
    path('admin-panel/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/add/', admin_views.admin_add_book, name='admin_add_book'),
    path('admin-panel/edit/<int:book_id>/', admin_views.admin_edit_book, name='admin_edit_book'),
    path('admin-panel/delete/<int:book_id>/', admin_views.admin_delete_book, name='admin_delete_book'),
