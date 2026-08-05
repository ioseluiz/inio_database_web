from django import forms

from .models import Estimador


TW_INPUT = (
    "mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full "
    "px-3 py-2 text-base leading-6 shadow-sm border border-gray-300 rounded-md"
)
TW_CHECKBOX = "h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"


class EstimadorForm(forms.ModelForm):
    class Meta:
        model = Estimador
        fields = ["name", "initials", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": TW_INPUT}),
            "initials": forms.TextInput(attrs={"class": TW_INPUT}),
            "is_active": forms.CheckboxInput(attrs={"class": TW_CHECKBOX}),
        }
        labels = {
            "name": "Nombre",
            "initials": "Iniciales",
            "is_active": "Activo",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.fields["initials"].required = True
        if not self.instance.pk:
            self.fields["is_active"].initial = True
