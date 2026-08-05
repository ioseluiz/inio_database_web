from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST

from .forms import EstimadorForm
from .models import Estimador


MOSTRAR_CHOICES = [
    ("activos", "Activos"),
    ("inactivos", "Inactivos"),
    ("todos", "Todos"),
]


def estimadores_view(request):
    query = (request.GET.get("q") or "").strip()
    mostrar = request.GET.get("mostrar") or "activos"
    if mostrar not in {c[0] for c in MOSTRAR_CHOICES}:
        mostrar = "activos"

    qs = Estimador.objects.all()
    if query:
        qs = qs.filter(Q(name__icontains=query) | Q(initials__icontains=query))
    if mostrar == "activos":
        qs = qs.filter(is_active=True)
    elif mostrar == "inactivos":
        qs = qs.filter(is_active=False)
    qs = qs.order_by("initials")

    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    prev_post = request.session.pop("estimador_form_data", None)
    request.session.pop("estimador_form_errors", None)
    if prev_post:
        create_form = EstimadorForm(prev_post)
        create_form.is_valid()
        open_add_modal = True
    else:
        create_form = EstimadorForm()
        open_add_modal = False

    edit_form_data = request.session.pop("estimador_edit_form_data", None)
    open_edit_modal_pk = request.session.pop("estimador_edit_form_pk", None)
    rows = []
    for obj in page_obj.object_list:
        if edit_form_data and open_edit_modal_pk == obj.pk:
            f = EstimadorForm(edit_form_data, instance=obj)
            f.is_valid()
        else:
            f = EstimadorForm(instance=obj)
        rows.append((obj, f))

    return render(
        request,
        "estimadores/estimadores.html",
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
def estimador_create_view(request):
    form = EstimadorForm(request.POST)
    if not form.is_valid():
        request.session["estimador_form_data"] = request.POST.dict()
        request.session["estimador_form_errors"] = form.errors.get_json_data()
        messages.error(request, "Revisa los errores del formulario.")
        return redirect("estimadores:estimadores")

    form.save()
    messages.success(request, "Estimador creado.")
    return redirect("estimadores:estimadores")


@require_POST
def estimador_update_view(request, pk):
    obj = get_object_or_404(Estimador, pk=pk)
    form = EstimadorForm(request.POST, instance=obj)
    if not form.is_valid():
        request.session["estimador_edit_form_data"] = request.POST.dict()
        request.session["estimador_edit_form_pk"] = pk
        messages.error(request, "Revisa los errores del formulario.")
        return redirect("estimadores:estimadores")

    form.save()
    messages.success(request, "Estimador actualizado.")
    return redirect("estimadores:estimadores")


@require_POST
def estimador_toggle_activo_view(request, pk):
    obj = get_object_or_404(Estimador, pk=pk)
    obj.is_active = not obj.is_active
    obj.save(update_fields=["is_active", "updated_at"])
    if obj.is_active:
        messages.success(request, f"Estimador '{obj.initials}' reactivado.")
    else:
        messages.success(request, f"Estimador '{obj.initials}' desactivado.")
    return redirect("estimadores:estimadores")
