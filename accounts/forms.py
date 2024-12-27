from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500'

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500'

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'profile_image', 'location', 'school', 'department',
            'grade', 'gender', 'height', 'weight', 'usual_size', 'bio'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'gender': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500'}),
            'is_school_info_public': forms.HiddenInput(),
            'is_personal_info_public': forms.HiddenInput()
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (forms.FileInput, forms.Textarea)):
                field.widget.attrs['class'] = 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500'
            else:
                field.widget.attrs['class'] = 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500'