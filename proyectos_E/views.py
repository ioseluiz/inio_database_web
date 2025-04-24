from django.shortcuts import render

from .models import Proyecto_E
from proyecto_E_Estimador.models import Proyecto_E_Estimador


def proyectos_e_view(request):
    # Query all Proyectos E
    proyectos_e_items = Proyecto_E.objects.prefetch_related('proyectos_E_estimador_relation__estimador').all()
    total_proyectos = len(proyectos_e_items)
    
    # Query the estimators of each project
    data_proyectos = []
    for item in proyectos_e_items:
        info = {}
        proyecto = item.codigo
        info['proyecto'] = proyecto
        info['title'] = item.title
        estimators = item.proyectos_E_estimador_relation.all()
        # Query all estimators in a project
        # print()
        # print(item.codigo)
        estimators_query = item.proyectos_E_estimador_relation.all()
        estimators = [x.estimador.initials for x in estimators_query]

        estimators_str = ",".join(estimators)
        info['estimadores'] = estimators_str
        data_proyectos.append(info)
    
    print('HOlaaaaaaaaaaaaaa')

    context = {"proyectos_e": data_proyectos, 'total_proyectos': total_proyectos }
    return render(request, "proyectos_e.html",context)
