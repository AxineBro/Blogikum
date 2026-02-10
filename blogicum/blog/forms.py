from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username) \
                .exclude(pk=self.instance.pk) \
                .exists():
            raise ValidationError('Этот логин уже занят.')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email) \
                .exclude(pk=self.instance.pk) \
                .exists():
            raise ValidationError('Этот email уже используется.')

        return email
