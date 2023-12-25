from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserChangeForm
from job_auth.models import UserProfile

class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['resume', 'company_id']

class CustomUserChangeForm(BaseForm, UserChangeForm):
    password=None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = self.instance
        if User.objects.filter(email=email).exclude(id=user.id).exists():
            raise forms.ValidationError('This email is already in use. Please use a different email address.')
        return email

class CustomAuthenticationForm(BaseForm, AuthenticationForm):
    pass

class UserSignupForm(BaseForm, UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(),
    )
    class Meta:
        model=User
        fields=['username', 'email']
        
    error_messages = {
        'password_mismatch': "Confirm Password did not match with Password..",
    }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email