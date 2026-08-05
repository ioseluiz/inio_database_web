from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST

from .forms import EspecificadorForm
from .models import Especificador


MOSTRAR_CHOICES = [
    ("activos", "Activos"),
    ("inactivos", "Inactivos"),
    ("todos", "Todos"),
]


def especificadores_view(request):
    query = (request.GET.get("q") or "").strip()
    mostrar = request.GET.get("mostrar") or "activos"
    if mostrar not in {c[0] for c in MOSTRAR_CHOICES}:
        mostrar = "activos"

    qs = Especificador.objects.all()
    if query:
        qs = qs.filter(Q(nombre__icontains=query) | Q(iniciales__icontains=query))
    if mostrar == "activos":
        qs = qs.filter(is_active=True)
    elif mostrar == "inactivos":
        qs = qs.filter(is_active=False)
    qs = qs.order_by("nombre")

    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    prev_post = request.session.pop("especificador_form_data", None)
    request.session.pop("especificador_form_errors", None)
    if prev_post:
        create_form = EspecificadorForm(prev_post)
        create_form.is_valid()
        open_add_modal = True
    else:
        create_form = EspecificadorForm()
        open_add_modal = False

    edit_form_data = request.session.pop("especificador_edit_form_data", None)
    open_edit_modal_pk = request.session.pop("especificador_edit_form_pk", None)
    rows = []
    for obj in page_obj.object_list:
        if edit_form_data and open_edit_modal_pk == obj.pk:
            f = EspecificadorForm(edit_form_data, instance=obj)
            f.is_valid()
        else:
            f = EspecificadorForm(instance=obj)
        rows.append((obj, f))

    return render(
        request,
        "especificadores/especificadores.html",
        {
            "page_obj": page_obj,
            "rows": rows,
            "total": qs.count(),
            "query": query,
            "mostrar": mostrar,
            "mostrar_choices": MOSTRAR_CHOICES,
            "create_form": create_form,
            "open_add_modal": open_add_modal,
            "open_edit_modal_pk": open_edit_modal_pk,
        },
    )


@require_POST
def especificador_create_view(request):
    form = EspecificadorForm(request.POST)
    if not form.is_valid():
        request.session["especificador_form_data"] = request.POST.dict()
        request.session["especificador_form_errors"] = form.errors.get_json_data()
        messages.error(request, "Revisa los errores del formulario.")
        return redirect("especificadores:especificadores")

    form.save()
    messages.success(request, "Especificador creado.")
    return redirect("especificadores:especificadores")


@require_POST
def especificador_update_view(request, pk):
    obj = get_object_or_404(Especificador, pk=pk)
    form = EspecificadorForm(request.POST, instance=obj)
    if not form.is_valid():
        request.session["especificador_edit_form_data"] = request.POST.dict()
        request.session["especificador_edit_form_pk"] = pk
        messages.error(request, "Revisa los errores del formulario.")
        return redirect("especificadores:especificadores")

    form.save()
    messages.success(request, "Especificador actualizado.")
    return redirect("especificadores:especificadores")


@require_POST
def especificador_toggle_activo_view(request, pk):
    obj = get_object_or_404(Especificador, pk=pk)
    obj.is_active = not obj.is_active
    obj.save(update_fields=["is_active", "updated_at"])
    if obj.is_active:
        messages.success(request, f"Especificador '{obj.nombre}' reactivado.")
    else:
        messages.success(request, f"Especificador '{obj.nombre}' desactivado.")
    return redirect("especificadores:especificadores")
