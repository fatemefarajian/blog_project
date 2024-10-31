from django import forms


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




