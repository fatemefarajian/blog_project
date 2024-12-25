from django import forms

from . import models
from .models import Comment, Post, User, Account


class TicketForms(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش'),
    )
    name = forms.CharField(max_length=100, required=True, label='نام')
    email = forms.EmailField(required=True, label='ایمیل')
    phone = forms.CharField(max_length=11, min_length=11, required=True, label='تلفن')
    message = forms.CharField(widget=forms.Textarea, required=True, label='پیام')
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, label='موضوع')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if not email.endswith('@example.com'):
                raise forms.ValidationError('ایمیل باید با @example.com پایان یابد.')
            else:
                return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            if not phone.startswith('09'):
                raise forms.ValidationError('شماره تلفن باید با پیش شماره09 شروع شود')
            if not phone.isnumeric():
                raise forms.ValidationError('شماره تلفن  وارد شده عددی نیست ')
            if not len(phone) == 11:
                raise forms.ValidationError('شماره تلفن باید 11 عدد باشد')
            else:
                return phone


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if text:
            if len(text) < 2:
                raise forms.ValidationError('متن نظر نمیتواند خیلی کوتاه باشد')
            else:
                return text


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)


class CreatePostForm(forms.ModelForm):
    image1 = forms.ImageField(label='تصویر اول')
    image2 = forms.ImageField(label='تصویر دوم')

    class Meta:
        model = Post
        fields = ['title', 'description', 'reading_time']


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, label='رمز')
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput, label='تکرار رمز')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('پسوررد ها مطابقت ندارند')
        else:
            return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['photo', 'date_of_birth', 'job', 'bio']
