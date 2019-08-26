from django import forms
from .models import Message, User, Article, Comment
from django.db.models import Q
from django.utils import timezone
import string


def photo_contraint(self):
    photo = self.cleaned_data['photo']
    if not type(photo) is str:
        max_size = 1024 * 1024  # 1MB
        if photo.size > max_size:
            self.add_error(
                'photo', 'The photo should be lower to 1MB->1024KB,'
                ' this photo has %sMB-->%sKo' %
                (int(photo.size / 1000 / 1000), int(photo.size / 1000)))
        else:
            pass
    else:
        pass
    return photo


class SigninForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class':
            'input',
            'placeholder':
            'Enter your username'
        })
        self.fields['email'].widget.attrs.update({
            'class':
            'input',
            'placeholder':
            'Enter your email'
        })
        self.fields['date_of_birth'].help_text = "Eg: 2010-10-10"
        self.fields['date_of_birth'].widget = forms.DateInput(
            attrs={'type': 'date'})
        self.fields['date_of_birth'].widget.attrs.update({
            'class': 'input',
        })
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].widget.attrs.update({
            'class': 'input',
        })
        self.fields['photo'].help_text = "*Optionnel"
        self.fields['first_name'].help_text = "*Optionnel"
        self.fields['first_name'].widget.attrs.update({
            'class': 'input',
        })
        self.fields['last_name'].help_text = "*Optionnel"
        self.fields['last_name'].widget.attrs.update({
            'class': 'input',
        })

    password_verification = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'Retape your password'
        }),
        required=True,
        help_text='Retape your password')

    class Meta:
        model = User
        fields = [
            'username', 'email', 'date_of_birth', 'password', 'photo',
            'first_name', 'last_name'
        ]

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        min_length = 4
        max_length = 30
        if len(username) < min_length:
            self.add_error(
                'username',
                'username is too short, min %s characters' % min_length)
        elif User.objects.filter(username=username):
            self.add_error('username', 'This username is already used')
        elif len(username) < min_length:
            self.add_error(
                'username',
                'username is too short, min %s characters' % min_length)
        elif len(username) > max_length:
            self.add_error(
                'username',
                'username is too long, max %s characters' % max_length)
        elif " " in username:
            self.add_error('username',
                           'username should not contains the space')
        elif username[0] in '0123456789':
            self.add_error('username',
                           'username should not begin with a number')
        else:
            pass
        for i in string.punctuation:
            if i in username:
                self.add_error(
                    'username',
                    'username should not contains a special character')
                break
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email):
            self.add_error('email', 'This email is already used')
        else:
            pass
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        min_length = 4
        if len(password) < min_length:
            self.add_error(
                'password',
                'password is too short, min %s characters' % min_length)
        else:
            pass
        return password

    def clean_photo(self):
        return photo_contraint(self)

    def clean_first_name(self, tag='first_name'):
        first_name = self.cleaned_data[tag]
        max_length = 30
        if first_name:
            if len(first_name) > max_length:
                self.add_error(
                    tag,
                    '%s is too long, max %s characters' % (tag, max_length))
            elif " " in first_name:
                self.add_error(tag, '%s should not contains the space' % tag)
            elif first_name[0] in '0123456789':
                self.add_error(tag, '%s should not begin with a number' % tag)
            else:
                pass
        else:
            pass
        return first_name

    def clean_last_name(self):
        return self.clean_first_name(tag='last_name')

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        if date_of_birth.year >= timezone.now().year:
            self.add_error('date_of_birth', 'You are too young.')
        return date_of_birth

    def clean(self):
        if 'password' not in self.cleaned_data:
            pass
        elif "password_verification" not in self.cleaned_data:
            pass
        else:
            password = self.cleaned_data['password']
            password_verification = self.cleaned_data['password_verification']
            if password != password_verification:
                self.add_error(
                    'password_verification', 'Password verification and'
                    ' password are different')
            else:
                pass


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username_or_email'].widget.attrs.update({
            'class':
            'input',
            'placeholder':
            'Type your Username or Email'
        })
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].widget.attrs.update({
            'class':
            'input',
            'placeholder':
            'Type your Password'
        })

    username_or_email = forms.CharField(required=True)
    password = forms.CharField(required=True)

    def clean(self):
        if 'username_or_email' not in self.cleaned_data:
            pass
        elif 'password' not in self.cleaned_data:
            pass
        else:
            username_or_email = self.cleaned_data['username_or_email'].lower()
            password = self.cleaned_data['password']
            user = User.objects.filter(
                Q(username=username_or_email) | Q(email=username_or_email))
            if user:
                user = user.filter(password=password)
                if user:
                    self.user = user[0]
                else:
                    self.add_error('password', 'password invalid')
            else:
                self.add_error('username_or_email', 'username|email invalid')

    def get_user(self):
        return self.user


class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contains'].widget = forms.Textarea(
            attrs={'style': 'height: 100%'})
        self.fields['contains'].widget.attrs.update({
            'class':
            'textarea',
            'placeholder':
            'Enter your message'
        })

    class Meta:
        model = Message
        fields = ['contains', 'photo']

    def clean_photo(self):
        return photo_contraint(self)


class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contains'].widget = forms.Textarea(
            attrs={'style': 'height: 100%'})
        self.fields['contains'].widget.attrs.update({
            'class':
            'textarea',
            'placeholder':
            'Enter your message'
        })

    class Meta:
        model = Article
        fields = ['contains', 'photo']

    def clean_photo(self):
        return photo_contraint(self)


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contains'].widget = forms.Textarea(
            attrs={'style': 'height: 100%'})
        self.fields['contains'].widget.attrs.update({
            'class':
            'textarea',
            'placeholder':
            'Enter your message'
        })

    class Meta:
        model = Comment
        fields = ['contains', 'photo']

    def clean_photo(self):
        return photo_contraint(self)


class ChangeDataUserForm(forms.Form):
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'placeholder': 'Enter the new first name',
                'type': 'text',
            }))
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'placeholder': 'Enter the new last name',
                'type': 'text',
            }))
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                'class': 'input',
                'placeholder': 'Enter the new date of birth',
                'type': 'date',
            }))
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'Enter your password'
        }),
        help_text='Enter your password to valid the modifications')

    def clean_date_of_birth(self):
        return SigninForm.clean_date_of_birth(self)

    def clean_first_name(self, tag='first_name'):
        return SigninForm.clean_first_name(self, tag=tag)

    def clean_last_name(self):
        return self.clean_first_name(tag='last_name')


class ChangePhotoForm(forms.Form):
    photo = forms.ImageField()

    def clean_photo(self):
        return photo_contraint(self)


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'Enter the old password'
        }))
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'Enter the new password'
        }))
    password_verification = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'Enter the new password'
        }))

    def clean_password(self):
        print(dir(self))
        return SigninForm.clean_password(self)

    def clean(self):
        if 'password' not in self.cleaned_data:
            pass
        elif 'password_verification' not in self.cleaned_data:
            pass
        else:
            password = self.cleaned_data['password']
            password_verification = self.cleaned_data['password_verification']
            if password != password_verification:
                self.add_error(
                    'password_verification', 'Password verification and'
                    ' password are different')
