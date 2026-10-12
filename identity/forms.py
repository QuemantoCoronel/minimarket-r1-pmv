from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(
            attrs={
                "id": "id_email",
                "autocomplete": "username",
                "autofocus": "autofocus",
                "required": "required",
                "aria-required": "true",
                "placeholder": "usuario@pmv.invalid",
            }
        ),
    )
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "id": "id_password",
                "autocomplete": "current-password",
                "required": "required",
                "aria-required": "true",
            }
        ),
    )
