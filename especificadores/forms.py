from django import forms

from .models import Especificador


TW_INPUT = (
    "mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full "
    "px-3 py-2 text-base leading-6 shadow-sm border border-gray-300 rounded-md"
)
TW_CHECKBOX = "h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"


class EspecificadorForm(forms.ModelForm):
    class Meta:
        model = Especificador
        fields = ["nombre", "iniciales", "is_active"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": TW_INPUT}),
            "iniciales": forms.TextInput(attrs={"class": TW_INPUT}),
            "is_active": forms.CheckboxInput(attrs={"class": TW_CHECKBOX}),
        }
        labels = {
            "nombre": "Nombre",
            "iniciales": "Iniciales",
            "is_active": "Activo",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nombre"].required = True
        self.fields["iniciales"].required = True
        if not self.instance.pk:
            self.fields["is_active"].initial = True
