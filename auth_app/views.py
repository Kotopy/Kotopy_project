from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            role = request.POST.get('role', 'user')
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)

            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})