from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from account.models import User


class UserAccountRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'image')


class UserAccountProfileForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'image')
