from django import forms
from kaizen_app.models import  Contact, Review



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'required': True}),
            'email': forms.EmailInput(attrs={'required': True}),
            'phone': forms.TextInput(attrs={'required': True}),
            'message': forms.Textarea(attrs={'required': True}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your review...'
            }),
        }
