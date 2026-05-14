from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from .forms import NewSignupForm

def signup(request):
    if request.method == 'POST':
        form = NewSignupForm(request.POST)
        if form.is_valid():
            user = form.save()  

            role = form.cleaned_data.get('role', 'user')
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)

            return redirect('login')
    else:
        form = NewSignupForm()
    return render(request, 'auth/signup.html', {'form': form})