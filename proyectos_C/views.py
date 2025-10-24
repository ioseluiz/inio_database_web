from django.shortcuts import render, redirect, get_object_or_404
from .models import Proyecto_CC
from django.db.models import Q, Value
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from datetime import timedelta, datetime

from proyecto_C_Especificador.models import Proyecto_C_Especificador
from especificadores.models import Especificador
from estimadores.models import Estimador
from secciones.models import Seccion
from master_projects.models import MasterProject

def proyectos_c_view(request):
    # Esta vista ahora maneja la visualización y el filtrado
    
    # Obtener valores de los parámetros GET
    query = request.GET.get('q')
    seccion_filter = request.GET.get('seccion')
    coordinador_filter = request.GET.get('coordinador')
    estado_filter = request.GET.get('estado')
    especificador_filter = request.GET.get('especificador')
    estimador_filter = request.GET.get('estimador')

    # Consulta base
    proyectos_c_items = Proyecto_CC.objects.prefetch_related(
        'proyectos_CC_estimador_relation__estimador',
        'proyectos_CC_especificador_relation__especificador'
    ).all()

    # Aplicar filtros si existen
    if query:
        proyectos_c_items = proyectos_c_items.filter(
            Q(codigo__icontains=query) | Q(title__icontains=query)
        ).distinct()
    
    if seccion_filter:
        proyectos_c_items = proyectos_c_items.filter(seccion=seccion_filter)
        
    if coordinador_filter:
        proyectos_c_items = proyectos_c_items.filter(coordinador=coordinador_filter)
        
    if estado_filter:
        proyectos_c_items = proyectos_c_items.filter(estado=estado_filter)
        
    if especificador_filter:
        proyectos_c_items = proyectos_c_items.filter(
            proyectos_CC_especificador_relation__especificador__id=especificador_filter
        )
        
    if estimador_filter:
        proyectos_c_items = proyectos_c_items.filter(
            proyectos_CC_estimador_relation__estimador__id=estimador_filter
        )

    # Ordenar resultados
    proyectos_c_items = proyectos_c_items.order_by('-fiscal_year','-codigo')
    
    # --- Obtener datos para los menús desplegables ---
    estimadores = Estimador.objects.filter(is_active=True)
    especificadores = Especificador.objects.filter(is_active=True)
    secciones = Seccion.objects.filter(is_active=True)
    
    # Obtener coordinadores únicos del modelo Proyecto_CC
    coordinadores = Proyecto_CC.objects.annotate(
        coord_nn=Coalesce('coordinador', Value(''))
    ).values_list('coord_nn', flat=True).distinct().order_by('coord_nn')
    coordinadores = [c for c in coordinadores if c] # Filtrar valores vacíos

    # Obtener estados desde las choices del modelo
    estados_choices = Proyecto_CC._meta.get_field('estado').choices 

    # Paginación
    paginator = Paginator(proyectos_c_items, 10) # Mostrar 10 proyectos por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    total_proyectos = proyectos_c_items.count() # Usar count() para eficiencia

    context = {
        'total_proyectos': total_proyectos, 
        "page_obj": page_obj, 
        "estimadores": estimadores, 
        "especificadors": especificadores,
        "secciones": secciones, 
        "estados": estados_choices, # Pasar las choices al template
        "coordinadores": coordinadores, # Nuevo contexto
        
        # Devolver los valores de filtro seleccionados al template
        'query': query,
        'seccion_filter': seccion_filter,
        'coordinador_filter': coordinador_filter,
        'estado_filter': int(estado_filter) if estado_filter else None,
        'especificador_filter': int(especificador_filter) if especificador_filter else None,
        'estimador_filter': int(estimador_filter) if estimador_filter else None,
    }
    return render(request, "proyectos_c/proyectos_c.html", context)

def proyectos_c_detail_view(request, pk):
    if request.method == "GET":
        proyecto = Proyecto_CC.objects.prefetch_related(
            'proyectos_CC_estimador_relation__estimador',
            'proyectos_CC_especificador_relation__especificador',
            'proyectos_CC_estimado_conceptual_cc__estimado_conceptual',
            'proyecto_cc_licitacion_set__licitacion',
            'proyecto_cc_sia_set__sia',
            'master_proyectos',
        ).get(pk=pk)
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



    
def proyecto_c_delete(request, pk):
    print('Delete...')
    context = {}
    # Delete an item
    proyecto = Proyecto_CC.objects.get(pk=pk)
    proyecto.delete()
    return redirect(reverse('proyectos_c:proyectos_c'))

# --- VISTA PARA DATOS DEL GANTT (MODIFICADA) ---
def proyecto_gantt_data(request, pk):
    proyecto = get_object_or_404(
        Proyecto_CC.objects.prefetch_related('proyecto_cc_licitacion_set__licitacion__contratos'), 
        pk=pk
    )
    tasks = []
    all_dates = []

    # --- FASE 1: DISEÑO ---
    if proyecto.fecha_entrada:
        start_date = proyecto.fecha_entrada
        end_date = proyecto.fecha_envio_FIO
        progress = 100
        nombre_tarea = "Diseño" # Default name

        # Si hay fecha de fin, calcula la duración y actualiza el nombre
        if end_date:
            # Asegurarse de que la fecha de fin no sea anterior a la de inicio
            if isinstance(end_date, datetime): end_date = end_date.date()
            if isinstance(start_date, datetime): start_date = start_date.date()
            
            if end_date >= start_date:
                duracion_diseno = (end_date - start_date).days
                nombre_tarea = f"Diseño ({duracion_diseno} días)"
            else: # Si la fecha de fin es inválida, trátala como si no existiera
                end_date = datetime.now().date()
                progress = 50
        else: # Si no hay fecha de fin, se asume que es una tarea en curso hasta hoy
            end_date = datetime.now().date()
            progress = 50 # Indicar que está en progreso

        tasks.append({
            'id': 'task_diseno',
            'name': nombre_tarea,
            'start': start_date.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d'),
            'progress': progress,
        })
        all_dates.append(start_date)
        if proyecto.fecha_envio_FIO:
            all_dates.append(end_date)



    # --- FASE 2: LICITACIÓN Y ADJUDICACIÓN ---
    for licitacion_rel in proyecto.proyecto_cc_licitacion_set.all():
        licitacion = licitacion_rel.licitacion
        lic_id = f'lic_{licitacion.pk}'
        
        # Barra de Licitación
        if licitacion.publication_date and licitacion.closed_date:
            duracion_licitacion = (licitacion.closed_date - licitacion.publication_date).days
            nombre_tarea = f"Licitación {licitacion.rfq} ({duracion_licitacion} días)"
            tasks.append({
                'id': lic_id,
                'name': nombre_tarea,
                'start': licitacion.publication_date.strftime('%Y-%m-%d'),
                'end': licitacion.closed_date.strftime('%Y-%m-%d'),
                'progress': 100, 
                'dependencies': 'task_diseno' # Depende de la fase de diseño
            })
            all_dates.extend([licitacion.publication_date, licitacion.closed_date])

            # Hito de Adjudicación
            for contrato in licitacion.contratos.all():
                if contrato.fecha_adjudicacion:
                    tasks.append({
                        'id': f'contrato_{contrato.pk}',
                        'name': f'Adjudicación ({contrato.numero_contrato})',
                        'start': contrato.fecha_adjudicacion.strftime('%Y-%m-%d'),
                        'end': contrato.fecha_adjudicacion.strftime('%Y-%m-%d'), # Mismo día para ser un hito
                        'progress': 100,
                        'dependencies': lic_id # Depende de la fase de licitación
                    })
                    all_dates.append(contrato.fecha_adjudicacion)

    if not all_dates:
        return JsonResponse([], safe=False)

    normalized_dates = []
    for d in all_dates:
        if isinstance(d, datetime):
            normalized_dates.append(d.date())
        else:
            normalized_dates.append(d)

    # Reducir el timedelta para eliminar el espacio vacío
    start_date = min(normalized_dates) - timedelta(days=1)
    end_date = max(normalized_dates) + timedelta(days=1)

    final_tasks = [
        {
            'id': 'gantt_start', 'name': '', 'start': start_date.strftime('%Y-%m-%d'),
            'end': start_date.strftime('%Y-%m-%d'), 'progress': 0, 'custom_class': 'hidden-task'
        },
        {
            'id': 'gantt_end', 'name': '', 'start': end_date.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d'), 'progress': 0, 'custom_class': 'hidden-task'
        }
    ]
    final_tasks.extend(tasks)
    return JsonResponse(final_tasks, safe=False)