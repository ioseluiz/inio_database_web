# accounts/forms.py

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    """
    Un formulario para crear nuevos usuarios con una contraseña repetida.
    """
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def clean_password2(self):
        # Comprueba que las dos contraseñas coincidan.
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def save(self, commit=True):
        # Guarda el usuario con la contraseña hasheada.
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# (Opcional) Un formulario para la página de edición, que es una buena práctica tener
class CustomUserChangeForm(forms.ModelForm):
    """Un formulario para actualizar usuarios. Incluye el hash de la contraseña."""
    password = ReadOnlyPasswordHashField(
        label='Password',
        help_text='No se pueden editar contraseñas en bruto aquí. Usa el <a href="../password/">formulario de cambio de contraseña</a>.'
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'is_active', 'is_staff', 'is_superuser')