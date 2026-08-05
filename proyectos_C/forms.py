from django import forms

from .models import Proyecto_CC
from especificadores.models import Especificador
from estimadores.models import Estimador
from SIA.models import tblProyectos
from proyectos_E.models import Proyecto_E
from secciones.models import Seccion


TW_INPUT = (
    "mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full "
    "px-3 py-2 text-base leading-6 shadow-sm border border-gray-300 rounded-md"
)
TW_SELECT = (
    "mt-1 block w-full pl-3 pr-10 py-2 text-base leading-6 border border-gray-300 "
    "focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 rounded-md"
)
TW_TEXTAREA = (
    "mt-1 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block "
    "w-full px-3 py-2 text-base leading-6 border border-gray-300 rounded-md"
)


class ProyectoCCForm(forms.ModelForm):
    estimadores = forms.ModelMultipleChoiceField(
        queryset=Estimador.objects.filter(is_active=True).order_by("initials"),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": TW_SELECT, "size": 6}),
        help_text="Mantén Ctrl (o Cmd en Mac) para seleccionar varios.",
    )
    especificadores = forms.ModelMultipleChoiceField(
        queryset=Especificador.objects.filter(is_active=True).order_by("iniciales"),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": TW_SELECT, "size": 6}),
        help_text="Mantén Ctrl (o Cmd en Mac) para seleccionar varios.",
    )
    sias = forms.ModelMultipleChoiceField(
        queryset=tblProyectos.objects.all().order_by("CodProyecto"),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": TW_SELECT, "size": 6}),
        label="SIA",
        help_text="Mantén Ctrl (o Cmd en Mac) para seleccionar varios.",
    )
    estimados_conceptuales = forms.ModelMultipleChoiceField(
        queryset=Proyecto_E.objects.all().order_by("-codigo"),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": TW_SELECT, "size": 6}),
        label="Estimados Conceptuales",
        help_text="Mantén Ctrl (o Cmd en Mac) para seleccionar varios.",
    )

    class Meta:
        model = Proyecto_CC
        fields = [
            "codigo",
            "title",
            "seccion",
            "coordinador",
            "fecha_entrada",
            "fecha_envio_FIO",
            "fecha_sol_fondos_aprob",
            "fecha_recibo_fondos_aprob",
            "asignacion_presup_final",
            "precio_acp",
            "estado",
            "comentarios",
        ]
        widgets = {
            "codigo": forms.TextInput(attrs={"class": TW_INPUT}),
            "title": forms.Textarea(attrs={"class": TW_TEXTAREA, "rows": 3}),
            "coordinador": forms.TextInput(attrs={"class": TW_INPUT}),
            "fecha_entrada": forms.DateInput(
                attrs={"class": TW_INPUT, "type": "date"}
            ),
            "fecha_envio_FIO": forms.DateInput(
                attrs={"class": TW_INPUT, "type": "date"}
            ),
            "fecha_sol_fondos_aprob": forms.DateTimeInput(
                attrs={"class": TW_INPUT, "type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "fecha_recibo_fondos_aprob": forms.DateTimeInput(
                attrs={"class": TW_INPUT, "type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "asignacion_presup_final": forms.NumberInput(
                attrs={"class": TW_INPUT, "step": "0.01"}
            ),
            "precio_acp": forms.NumberInput(
                attrs={"class": TW_INPUT, "step": "0.01"}
            ),
            "estado": forms.Select(attrs={"class": TW_SELECT}),
            "comentarios": forms.Textarea(
                attrs={"class": TW_TEXTAREA, "rows": 3}
            ),
        }
        labels = {
            "fecha_envio_FIO": "Fecha de Envío a FIO",
            "fecha_sol_fondos_aprob": "Fecha Solicitud Fondos Aprobados",
            "fecha_recibo_fondos_aprob": "Fecha Recibo Fondos Aprobados",
            "asignacion_presup_final": "Asignación Presupuestaria Final",
            "precio_acp": "Precio ACP",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        seccion_choices = [("", "---")] + [
            (s.name, s.name)
            for s in Seccion.objects.filter(is_active=True).order_by("name")
        ]
        self.fields["seccion"] = forms.ChoiceField(
            choices=seccion_choices,
            required=False,
            widget=forms.Select(attrs={"class": TW_SELECT}),
            label="Sección",
        )
        self.fields["codigo"].required = True
        self.fields["fecha_sol_fondos_aprob"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["fecha_recibo_fondos_aprob"].input_formats = ["%Y-%m-%dT%H:%M"]
