from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Proyecto_E
from proyecto_E_Estimador.models import Proyecto_E_Estimador


def proyectos_e_view(request):
    # Query all Proyectos E
    proyectos_e_items = Proyecto_E.objects.prefetch_related('proyectos_E_estimador_relation__estimador').all()
    paginator = Paginator(proyectos_e_items, 10) # Show 25 projects per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    total_proyectos = len(proyectos_e_items)
    
    # Query the estimators of each project
    # data_proyectos = []
    # for item in proyectos_e_items:
    #     info = {}
    #     proyecto = item.codigo
    #     info['proyecto'] = proyecto
    #     info['title'] = item.title
    #     estimators = item.proyectos_E_estimador_relation.all()
    #     # Query all estimators in a project
    #     # print()
    #     # print(item.codigo)
    #     estimators_query = item.proyectos_E_estimador_relation.all()
    #     estimators = [x.estimador.initials for x in estimators_query]

    #     estimators_str = ",".join(estimators)
    #     info['estimadores'] = estimators_str
    #     data_proyectos.append(info)
    
    print('HOlaaaaaaaaaaaaaa')

    context = {'total_proyectos': total_proyectos, "page_obj": page_obj }
    return render(request, "proyectos_e.html",context)

def proyectos_list_view(request):
    """
    View to list projects with search across codigo and title, with pagination
    """
    proyectos_list = Proyecto_E.objects.all() # Start with all proyectos E
    query = request.GET.get('q') # Get the search query from URL (?q=...)

    if query:
        # Use Q objects to search across multiple fields with OR logic
        #icontains makes the search case-insensitive
        proyectos_list = proyectos_list.filter(
            Q(codigo__icontains=query) | Q(title__icontains=query)
        ).distinct() # use distinct() if your Q objects might cause duplicates

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

    context = {
        'proyectos': proyectos,
        'query': query, # Pass the query back to the template to display in search bar
        'page_obj': proyectos # Pass the page object for pagination controls
    }

    return render(request, '')


# -- Detail View --
def proyecto_E_detail_view(request, pk):
    proyecto = Proyecto_E.objects.prefetch_related('proyectos_E_estimador_relation__estimador').get(pk=pk)
    template_name = "proyecto_e_detail.html"

    context = {"proyecto": proyecto}
    return render(request, template_name, context)


def item_search_view(request):
    search_query = request.GET.get('q','') # Get search query from URL parameter 'q'

    # Filter items based on the search query (case-insensitive)
    if search_query:
        items =Proyecto_E.objects.prefetch_related('proyectos_E_estimador_relation__estimador').filter(title__icontains=search_query)
    else:
        items = Proyecto_E.objects.none()

    context = {}

    # Check if the request is from HTMX
    if request.htmx:
        # If it's an HTMX request, render only the partial template
        template_name = '_item_results_partial_html'
    else:
        # If it's a normal request, render the full page template
        template_name = 'proyectos_e.html'

    return render(request, template_name, context)

