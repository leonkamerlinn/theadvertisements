from django import forms
from .models import User, Group, Post, Replay, Roles
from django.shortcuts import get_object_or_404
from django.core import validators
from .validators import check_if_email_exist_validator, name_validator, phone_number_validator, password_validator, check_if_is_email_verified
import bcrypt


class LoginForm(forms.Form):
    email = forms.CharField(label='', max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        }
    ), validators=[check_if_email_exist_validator, check_if_is_email_verified])

    password = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        }
    ))

    def is_logged_in(self):
        email = self.cleaned_data.get('email')
        plainPassword = self.cleaned_data.get('password')
        user = get_object_or_404(User, email=email)
        try:
            return bcrypt.checkpw(plainPassword.encode('utf-8'), user.password.encode('utf-8'))
        except:
            return False



class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(label='', max_length=25, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'First name'
        }
    ), validators=[name_validator])

    last_name = forms.CharField(label='', max_length=25, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Last name'
        }
    ), validators=[name_validator])

    email = forms.CharField(label='', max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Email address'
        }
    ), validators=[validators.validate_email])

    phone_number = forms.CharField(label='', max_length=13, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Phone number'
        }
    ), validators=[phone_number_validator])

    password = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        }
    ), validators=[password_validator])

    repeat_password = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Repeat password'
        }
    ))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']

    def clean_repeat_password(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')
        if password != repeat_password:
            raise forms.ValidationError('Password and confirm password does not match')






class TokenExpiredForm(forms.Form):
    email = forms.CharField(label='', max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        }
    ), validators=[validators.validate_email, check_if_email_exist_validator])

    def clean_email(self):
        email_passed = self.cleaned_data.get('email')

        return email_passed

class ForgotPasswordForm(forms.Form):
    email = forms.CharField(label='', max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        }
    ), validators=[validators.validate_email, check_if_email_exist_validator])

    def clean_email(self):
        email_passed = self.cleaned_data.get('email')

        return email_passed



class ResetPasswordForm(forms.Form):
    password = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        }
    ), validators=[password_validator])

    repeat_password = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Repeat password'
        }
    ))

    def clean_repeat_password(self):
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')
        if password != repeat_password:
            raise forms.ValidationError('Password and confirm password does not match')


    def change_password(self, email):
        if User.objects.filter(email=email).count() == 1:
            user = User.objects.get(email=email)
            password = self.cleaned_data.get('password')
            user.password = password
            user.save()
            return True

        return False

class GroupForm(forms.ModelForm):

    name = forms.CharField(label='', max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control col',
            'placeholder': 'Group name'
        }
    ))
    description = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control col',
            'placeholder': 'Description',
            'rows': 3
        }
    ))

    owner = forms.ModelChoiceField(queryset=User.objects.all())


    def __init__(self, *args, **kwargs):

        super(GroupForm, self).__init__(*args, **kwargs)
        choices = [(user.id, user) for user in User.objects.all()]
        self.fields['users'].choices = choices


    class Meta:
        model = Group
        fields = ['name', 'description', 'users', 'owner']
        widgets = {
            'users': forms.CheckboxSelectMultiple
        }

class PostForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control col',
            'placeholder': 'Write post',
            'rows': 3,
            'style': 'width: 50%;'
        }
    ))

    owner = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ['text', 'group', 'owner']


class ReplayForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control col',
            'placeholder': 'Write replay',
            'rows': 2,
            'style': 'width: 30%;'
        }
    ))

    subject = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = Replay
        fields = ['text', 'post', 'subject']

class NotesForm(forms.ModelForm):
    owner = forms.ModelChoiceField(queryset=User.objects.all())
    name = forms.CharField(label='', max_length=255, widget=forms.TextInput(
        attrs={
            'class': 'form-control col',
            'placeholder': 'Group name'
        }
    ))
    description = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control col',
            'placeholder': 'Description',
            'rows': 4
        }
    ))


    class Meta:
        model = Roles
        fields = ['owner', 'name', 'description']