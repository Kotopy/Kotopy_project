from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    role = forms.ChoiceField(choices=[('user', 'User'), ('admin', 'Admin')], required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']  
        user.last_name = self.cleaned_data['last_name']    

        role = self.cleaned_data.get('role', 'user')
        if role == 'admin':
            user.is_staff = True
            user.is_superuser = True

        if commit:
            user.save()
        return user