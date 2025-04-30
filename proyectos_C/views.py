from django.shortcuts import render

def proyectos_c_view(request):
    context = {}
    return render(request, "proyectos_c/proyectos_c.html", context)

def proyectos_c_detail_view(request):
    context = {}
    return render(request, "proyectos_c/proyectos_c_detail.html", context)

