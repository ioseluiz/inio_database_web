# from django.shortcuts import render
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.urls import reverse_lazy
# from django.views.generic import (
#     ListView,
#     DetailView,
#     CreateView,
#     UpdateView,
#     DeleteView,
# )

# from .models import SIA

# def sia_list_view(request):
#     if request.method == "GET":
#         # Query all SIA
#         sia_items = SIA.objects.all().order_by('-Fiscal','-CodProyecto')
#         print(len(sia_items))
#         paginator = Paginator(sia_items, 10) # Show 10 projects per page
#         page_number = request.GET.get("page")
#         page_obj = paginator.get_page(page_number)
#         total_sias = len(sia_items)
         

#         context = {'total_sias': total_proyectos, "page_obj": page_obj, "estimadores":estimadores, "especificadors": especificadores,"secciones": secciones, "estados": estados}
#         return render(request, "proyectos_c/proyectos_c.html",context)

#     # Query all Proyectos CC
    
#     paginator = Paginator(proyectos_c_items, 10) # Show 25 projects per page
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     total_proyectos = len(proyectos_c_items)

#     context = {'total_proyectos': total_proyectos, "page_obj": page_obj, "estimadores":estimadores, "secciones": secciones, "estados": estados}
#     return render(request, "proyectos_c/proyectos_c.html", context)


