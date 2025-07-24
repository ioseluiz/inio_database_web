from django.shortcuts import render, redirect
from .models import Proyecto_CC
from django.db.models import Q
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from proyecto_C_Especificador.models import Proyecto_C_Especificador
from especificadores.models import Especificador
from estimadores.models import Estimador
from secciones.models import Seccion

def proyectos_c_view(request):
    if request.method == "GET":
        # Query all Proyectos E
        proyectos_c_items = Proyecto_CC.objects.prefetch_related('proyectos_CC_estimador_relation__estimador').prefetch_related("proyectos_CC_especificador_relation").all().order_by('-fiscal_year','-codigo')
        print(len(proyectos_c_items))
        estimadores = Estimador.objects.filter(is_active=True)
        especificadores = Especificador.objects.filter(is_active=True)
        secciones = Seccion.objects.filter(is_active=True)
        estados = ["ACTIVO","CANCELADO","INACTIVO","TERMINADO"]
        paginator = Paginator(proyectos_c_items, 10) # Show 10 projects per page
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        total_proyectos = len(proyectos_c_items)
         

        context = {'total_proyectos': total_proyectos, "page_obj": page_obj, "estimadores":estimadores, "especificadors": especificadores,"secciones": secciones, "estados": estados}
        return render(request, "proyectos_c/proyectos_c.html",context)

    # Query all Proyectos CC
    
    paginator = Paginator(proyectos_c_items, 10) # Show 25 projects per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    total_proyectos = len(proyectos_c_items)

    context = {'total_proyectos': total_proyectos, "page_obj": page_obj, "estimadores":estimadores, "secciones": secciones, "estados": estados}
    return render(request, "proyectos_c/proyectos_c.html", context)

def proyectos_c_detail_view(request, pk):
    if request.method == "GET":
        proyecto = Proyecto_CC.objects.prefetch_related('proyectos_CC_estimador_relation__estimador',  'proyectos_CC_especificador_relation__especificador').prefetch_related("proyectos_CC_estimador_relation").get(pk=pk)
        template_name = "proyectos_c/proyecto_c_detail.html"

        context = {"proyecto": proyecto}
        return render(request, template_name, context)


def proyectos_list_view(request):
    """
    View to list projects with search across codigo and title, with pagination
    """
    
    proyectos_list = Proyecto_CC.objects.prefetch_related('proyectos_CC_especificador_relation').prefetch_related("proyectos_CC_estimador_relation").all().order_by('-fiscal_year', '-codigo') # Start with all proyectos CC
    query = request.GET.get('q') # Get the search query from URL (?q=...)
    print(query)
    if query:
        # Use Q objects to search across multiple fields with OR logic
        #icontains makes the search case-insensitive
        proyectos_list = proyectos_list.filter(
            Q(codigo__icontains=query) | Q(title__icontains=query)
        ).distinct() # use distinct() if your Q objects might cause duplicates

    total_proyectos = len(proyectos_list)

    # --- Pagination ---
    paginator = Paginator(proyectos_list, 10) # Show 10 proyectos E per page
    page_number = request.GET.get('page')

    try:
        proyectos = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        proyectos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        proyectos = paginator.page(paginator.num_pages)

    especificadores = Especificador.objects.filter(is_active=True)

    context = {
        'proyectos': proyectos,
        'query': query, # Pass the query back to the template to display in search bar
        'page_obj': proyectos, # Pass the page object for pagination controls
        'total_proyectos': total_proyectos,
        'especificadores': especificadores,
    }

    return render(request, 'proyectos_c/proyectos_c_list.html', context)


# -- Detail View --
def proyecto_C_detail_view(request, pk):
    if request.method == "GET":
        proyecto = Proyecto_CC.objects.prefetch_related('proyectos_C_estimador_relation__estimador', 'proyectos_CC_especificador_relation__especificador').get(pk=pk)
        template_name = "proyecto_c_detail.html"

        context = {"proyecto": proyecto}
        return render(request, template_name, context)
    
def proyecto_c_delete(request, pk):
    print('Delete...')
    context = {}
    # Delete an item
    proyecto = Proyecto_CC.objects.get(pk=pk)
    proyecto.delete()
    return redirect(reverse('proyectos_c:proyectos_c'))


