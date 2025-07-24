from django.shortcuts import render
from .models import Contrato
from django.db.models import Q, F
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def contratos_view(request):
    if request.method == "GET":
        # Query all Contrato objects
        contrato_items = Contrato.objects.all().order_by(F('fecha_adjudicacion').desc(nulls_last=True))
        # estimadores = Estimador.objects.filter(is_active=True)
        # especificadores = Especificador.objects.filter(is_active=True)
        # secciones = Seccion.objects.filter(is_active=True)
        # estados = ["ACTIVO","CANCELADO","INACTIVO","TERMINADO"]
        paginator = Paginator(contrato_items, 10) # Show 10 projects per page
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        total_contratos = len(contrato_items)
            

        context = {'total_contratos': total_contratos, "page_obj": page_obj}
        return render(request, "contratos/contratos.html",context)
    
    # Query all Contratos
    
    paginator = Paginator(contrato_items, 10) # Show 25 projects per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    total_contratos = len(contrato_items)

    context = {'total_contratos': total_contratos, "page_obj": page_obj}
    return render(request, "contratos/contratos.html", context)
     
    

def contratos_detail_view(request):
    pass

def contratos_list_view(request):
    """
    View to list projects with search across codigo and title, with pagination
    """
    contratos_list = Contrato.objects.all().order_by(F('fecha_adjudicacion', 'fiscal_year','fiscal_month').desc(nulls_last=True))
    query = request.GET.get('q') # Get the search query from URL (?q=...)
    if query:
        # Use Q objects to search across multiple fields with OR logic
        #icontains makes the search case-insensitive
        contratos_list = contratos_list.filter(
            Q(numero_contrato__icontains=query) | Q(description__icontains=query)
        ).distinct() # use distinct() if your Q objects might cause duplicates

    total_contratos = len(contratos_list)

    # --- Pagination ---
    paginator = Paginator(contratos_list, 10) # Show 10 contratos per page
    page_number = request.GET.get('page')

    try:
        proyectos = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        proyectos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contratos = paginator.page(paginator.num_pages)

    context = {
        'contratos': contratos,
        'query': query, # Pass the query back to the template to display in search bar
        'page_obj': proyectos, # Pass the page object for pagination controls
        'total_contratos': total_contratos
    }

    return render(request, 'contratos/contratos_list.html', context)

def contratos_delete_view(request):
    pass
