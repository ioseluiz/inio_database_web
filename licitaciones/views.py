from django.shortcuts import render, get_object_or_404
from django.db.models import Q, F, Count
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .models import Licitacion

def licitaciones_view(request):
    """
    Vista optimizada para mostrar todas las licitaciones con paginacion.
    """
    base_query = Licitacion.objects.select_related('category').prefetch_related(
        'enmiendas',
        'propuestas'
    ).annotate(
        cantidad_enmiendas=Count('enmiendas', distinct=True),
        cantidad_proponentes=Count('propuestas__bid_proponente_id', distinct=True)
    )
    licitacion_items = base_query.order_by(F('publication_date').desc(nulls_last=True))
    paginator = Paginator(licitacion_items, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'total_licitaciones': paginator.count,
        'page_obj': page_obj,
        'estados': Licitacion.ESTADO_LIC_CHOICES
    }
    return render(request, "licitaciones/licitaciones.html", context)
   


def licitaciones_detail_view(request, pk):
    """
    Muestra el detalle de una licitacion especifica, incluyendo sus propuestas y enmiendas
    """
    licitacion = get_object_or_404(
        Licitacion.objects.prefetch_related('propuestas', 'enmiendas'), pk=pk
    )
    context = {
        'licitacion': licitacion
    }

    return render(request, 'licitaciones/licitaciones_detail.html', context)

def licitaciones_list_view(request):
    """
    View para listar licitaciones con busqueda por RFQ y descripcion con paginacion
    y carga optimizada de datos relacionados.
    """
    base_query = Licitacion.objects.select_related('category').prefetch_related(
        'enmiendas',
        'propuestas'
    ).annotate(
        cantidad_enmiendas=Count('enmiendas', distinct=True),
        cantidad_proponentes=Count('propuestas__bid_proponente_id', distinct=True)
    )

    licitaciones_list = base_query.order_by(F('publication_date').desc(nulls_last=True))
    query = request.GET.get('q', '') # Obtiene el parametro de la URL
    estado_filter = request.GET.get('estado','')

    if query:
        # icontains hace la busqueda insensible a mayusculas/minusculas
        licitaciones_list = licitaciones_list.filter(
            Q(rfq__icontains=query) | Q(gral_desc__icontains=query)
        ).distinct()

    if estado_filter:
        licitaciones_list = licitaciones_list.filter(estado_lic=estado_filter)

    # --- Pagination ---
    paginator = Paginator(licitaciones_list, 10) # Show 10 contratos per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'licitaciones': page_obj,
        'query': query,
        'total_licitaciones': paginator.count,
        'estados': Licitacion.ESTADO_LIC_CHOICES,
        'page_obj': page_obj
    }
    return render(request, "licitaciones/licitaciones.html", context)





