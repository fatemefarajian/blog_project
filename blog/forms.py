from django import forms


class TicketForms(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش'),
    )
    name = forms.CharField(max_length=100, required=True, label='نام')
    message = forms.CharField(widget=forms.Textarea, required=True, label='پیام')
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, label='موضوع')
