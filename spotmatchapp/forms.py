from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from activation import send_activation
from threading import Thread

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="E-Mail")

    class Meta:
        model = User
        fields = ("username", "email", )

    def clean_email(self):
        useremail = self.cleaned_data["email"]

        try:
            User.objects.get(email=useremail)
        except User.DoesNotExist:
            return useremail

        raise forms.ValidationError("You have already registered with this email address")

    def save(self):
        user = super(RegisterForm, self).save(commit=False)
        user.is_active = False
        
        thread = Thread(target=send_activation,  args=[user])
        thread.setDaemon(True)
        thread.start()
        
        send_activation(user)
        user.save()
