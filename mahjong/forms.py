from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from mahjong.models import Profile

MAX_UPLOAD_SIZE = 2500000


class ProfileForm(forms.ModelForm):
    # 是否写clean
    class Meta:
        model = Profile
        fields = ('profile_picture', )
        widgets = {
            'profile_picture': forms.FileInput(attrs={'id': 'id_profile_picture'}),
        }

    def clean_picture(self):
        picture = self.cleaned_data['profile_picture']
        if not picture or not hasattr(picture, 'content_type'):
            raise forms.ValidationError('You must upload a picture')
        if not picture.content_type or not picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label='Username')
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(), label='Password')

    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'id_username'}))
    password = forms.CharField(max_length=200,
                               label='Password',
                               widget=forms.PasswordInput(attrs={'id': 'id_password'}))
    confirm_password = forms.CharField(max_length=200,
                                       label='Confirm password',
                                       widget=forms.PasswordInput(attrs={'id': 'id_confirm_password'}))
    email = forms.CharField(max_length=50,
                            widget=forms.EmailInput(attrs={'id': 'id_email'}))
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'id_first_name'}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'id_last_name'}))

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username
