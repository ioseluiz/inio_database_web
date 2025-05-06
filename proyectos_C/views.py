from django.shortcuts import render
from .models import Proyecto_CC
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def proyectos_c_view(request):
    # Query all Proyectos CC
    proyectos_c_items = Proyecto_CC.objects.prefetch_related('proyectos_CC_estimador_relation__estimador').all()
    paginator = Paginator(proyectos_c_items, 10) # Show 25 projects per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    total_proyectos = len(proyectos_c_items)

    context = {}
    return render(request, "proyectos_c/proyectos_c.html", context)

def proyectos_c_detail_view(request):
    context = {}
    return render(request, "proyectos_c/proyectos_c_detail.html", context)

