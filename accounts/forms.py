from django.forms import ModelForm, PasswordInput, ValidationError, CharField
from django.contrib.auth.models import User

class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]
        widgets = {
            "password": PasswordInput,
        }
    
    repeat_password = CharField(label='Repeat password', \
                                widget=PasswordInput, \
                                required = True)

    field_order = ["username", "email", "password", "repeat_password", \
                   "first_name", "last_name"]

    def clean(self):
        """
        Override clean() to validate that the password and
        repeat_password fields have the same string.
        """
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")

        # If both values were validated successfully, perform the check
        if password and repeat_password:
            if password != repeat_password:
                err = ValidationError(
                    "The password must be the same in both fields.",
                    code = "password_mismatch"
                )

                self.add_error("repeat_password", err)

    def save(self, commit=True):
        """
        Override so that the password will be hased using set_password
        before it is stored in the model
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user





    