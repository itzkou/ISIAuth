from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from dashboard.models import User, Club


class ClubSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic  # to ensure atomicity of all actions
    def save(self):
        # this is how we override save method / commit =False because we are processing the object before daving to DB
        user = super().save(commit=False)
        user.is_club = True  # setting the flag
        user.save()  # saving
        club = Club.objects.create(user=user)
        return user
