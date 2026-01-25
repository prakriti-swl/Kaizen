from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from kaizen_app.models import  Contact, UserProfile



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

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows':2}), required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone", "address", "image", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit)
        profile = UserProfile.objects.get(user=user)
        profile.phone = self.cleaned_data.get("phone")
        profile.address = self.cleaned_data.get("address")
        if self.cleaned_data.get("image"):
            profile.image = self.cleaned_data.get("image")
        profile.save()
        return user
