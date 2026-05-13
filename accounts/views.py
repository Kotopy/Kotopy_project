from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile
from books.models import BorrowedBook

# انا سمية علي 
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # Sync role with staff/superuser status or 'admin' group
    is_admin = request.user.is_staff or request.user.is_superuser or request.user.groups.filter(name='admin').exists()
    
    if is_admin:
        if profile.role != 'admin':
            profile.role = 'admin'
            profile.save()
    elif profile.role == 'admin':
        # If they were admin but are no longer staff/superuser/group-admin, demote to user
        profile.role = 'user'
        profile.save()

    borrowed_count = BorrowedBook.objects.filter(user=request.user).count()

    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'borrowed_count': borrowed_count,
        'page': 'profile',
    })


@login_required
def edit_profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name  = request.POST.get('last_name', '').strip()
        user.email      = request.POST.get('email', '').strip()
        user.save()
        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('profile')

    return render(request, 'accounts/edit_profile.html', {
        'profile': profile,
        'page': 'profile',
    })


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('profile')
        else:
            for error in form.errors.values():
                messages.error(request, error.as_text())
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {
        'form': form,
        'page': 'profile',
    })
