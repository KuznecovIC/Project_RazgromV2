from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
from .models import UserProfile

User = get_user_model()

class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-input'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Этот email уже используется")
        return email

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'status', 'custom_status']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-input', 
                'rows': 4, 
                'placeholder': 'Расскажите о себе...'
            }),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'custom_status': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ваш статус...'
            }),
        }
        labels = {
            'bio': 'Биография',
            'status': 'Статус',
            'custom_status': 'Пользовательский статус',
        }

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ваш email'
        })
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Новый пароль'
        }),
    )
    new_password2 = forms.CharField(
        label="Подтвердите пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Повторите пароль'
        }),
    )