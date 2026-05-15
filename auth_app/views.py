from .forms import NewSignupForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from accounts.models import Profile

def signup(request):
    if request.method == 'POST':
        form = NewSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            return redirect('login')
    else:
        form = NewSignupForm()
    return render(request, 'auth/signup.html', {'form': form})