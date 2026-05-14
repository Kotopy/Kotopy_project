from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from accounts.models import Profile

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            role = request.POST.get('role', 'user')

            # Add to group
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)

            # Create Profile
            Profile.objects.get_or_create(user=user, defaults={'role': role})

            # If admin, give is_staff
            if role == 'admin':
                user.is_staff = True
                user.save()

            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})