from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseNotAllowed
from django.db.models import Q
from django.urls import reverse
from .models import Proyecto_E
from proyecto_E_Estimador.models import Proyecto_E_Estimador
from estimadores.models import Estimador
from secciones.models import Seccion
from datetime import datetime

def convert_date_format(date_string_mdy: str)-> str | None:
    try:
        date_object = datetime.strptime(date_string_mdy, "%m/%d/%Y")
        date_string_ymd = date_object.strftime("%Y-%m-%d")
        return date_string_ymd
    except ValueError:
        print(f"Error: The date string '{date_string_ymd}' is not in 'MM/DD/YYYY' format or is an invalid date.")
        return None
    except Exception as e:
        print(f"An unexpected error ocurred: {e}")
        return None

def proyectos_e_view(request):
    if request.method == "GET":
        # Query all Proyectos E
        proyectos_e_items = Proyecto_E.objects.prefetch_related('proyectos_E_estimador_relation__estimador').all()
        estimadores = Estimador.objects.filter(is_active=True)
        secciones = Seccion.objects.filter(is_active=True)
        estados = ["ACTIVO","CANCELADO","INACTIVO","TERMINADO"]
        paginator = Paginator(proyectos_e_items, 10) # Show 10 projects per page
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        total_proyectos = len(proyectos_e_items)
         

        context = {'total_proyectos': total_proyectos, "page_obj": page_obj, "estimadores":estimadores, "secciones": secciones, "estados": estados}
        return render(request, "proyectos_e.html",context)
    
    elif request.method == 'POST':
        # Create a new item from HTML form data
        codigo = request.POST.get('codigo')
        titulo = request.POST.get('title')
        fecha_entrada = request.POST.get('fecha_entrada')
        print(fecha_entrada)
        # if fecha_entrada:
        #     fecha_entrada = convert_date_format(fecha_entrada)
        fecha_salida = request.POST.get('fecha_salida')
        print(fecha_salida)
        if fecha_salida == "":
            fecha_salida = None
        seccion = request.POST.get('seccion')
        coordinador = request.POST.get('coordinador')
        comentarios = request.POST.get('comentarios')
        fiscal_year = request.POST.get('fiscal_year')
        asignacion_presup = request.POST.get('asignacion_presup')
        if asignacion_presup == "":
            asignacion_presup = None
        estimadores = request.POST.getlist('estimador')
        # Get the estimador from initials
        estimador_objects = []
        for estimador in estimadores:
            estimador_object = Estimador.objects.get(initials=estimador)
            estimador_objects.append(estimador_object)
        status = request.POST.get('status')

        # return JsonResponse({"message": "Test POST Method"})

        errors = {}
        if not codigo:
            errors['codigo'] = 'Codigo no puede estar vacio.'
        if not titulo:
            errors['titulo'] = 'Titulo no puede estar vacio.'

        if errors:
            return JsonResponse({"error": errors}, status=400) # 400 Bad Request
        
        try:
            # Create Proyecto E
            proyecto_e = Proyecto_E.objects.create(
                codigo=codigo,
                title=titulo, 
                fecha_entrada=fecha_entrada,
                 fecha_salida=fecha_salida,
                  seccion=seccion,
                    coordinador=coordinador,
                    comentarios=comentarios,
                    fiscal_year=fiscal_year,
                    asignacion_presup=asignacion_presup)
            print('Proyecto E creado correctamente.')
            
            # Create Proyecto E - Estimador
            for obj in estimador_objects:
                proyecto_e_estimador = Proyecto_E_Estimador.objects.create(
                    proyecto_e = proyecto_e,
                    estimador = obj
                )
            print('Proyecto E - Estimador creado correctamente.')
            
            response_data = {
                'id': str(proyecto_e.id),
                'codigo': proyecto_e.codigo,
                'title': proyecto_e.title,
                'fecha_entrada': proyecto_e.fecha_entrada,
                'fecha_salida': proyecto_e.fecha_salida,
                'seccion': proyecto_e.seccion,
                'coordinador': proyecto_e.coordinador,
                'fiscal_year': proyecto_e.fiscal_year,
                'asignacion_presup':proyecto_e.asignacion_presup,
            }
            # return JsonResponse(response_data, status=201) # 201 Created
            return redirect(reverse('proyectos_e:proyectos_e'))

        except Exception as e:
            # Catch any other potential errors during save
            return JsonResponse({"error": f"Could not save proyecto_e: {str(e)}"}, status=500)
    else:
        return JsonResponse({"message": "Mehod not Allowed!"})
            
        

def proyectos_list_view(request):
    """
    View to list projects with search across codigo and title, with pagination
    """
    
    proyectos_list = Proyecto_E.objects.prefetch_related('proyectos_E_estimador_relation__estimador').all() # Start with all proyectos E
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

    context = {
        'proyectos': proyectos,
        'query': query, # Pass the query back to the template to display in search bar
        'page_obj': proyectos, # Pass the page object for pagination controls
        'total_proyectos': total_proyectos
    }

    return render(request, 'proyectos_e/proyectos_e_list.html', context)


# -- Detail View --
def proyecto_E_detail_view(request, pk):
    if request.method == "GET":
        proyecto = get_object_or_404(
            Proyecto_E.objects.prefetch_related(
                'proyectos_E_estimador_relation__estimador',
                'horas_de_apoyo' # Usamos el related_name que definimos en models.py
            ), 
            pk=pk
        )
        template_name = "proyecto_e_detail.html"

        context = {"proyecto": proyecto}
        return render(request, template_name, context)
    
def proyecto_e_delete(request, pk):
    print('Delete...')
    context = {}
    # Delete an item
    proyecto = Proyecto_E.objects.get(pk=pk)
    proyecto.delete()
    return redirect(reverse('proyectos_e:proyectos_e'))

def proyecto_e_update(request, pk):
    pass
        

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

