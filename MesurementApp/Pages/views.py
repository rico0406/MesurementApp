from django.shortcuts import render
from Inspecao.models import Inspection

# Create your views here.
def home_view(request):
    #../insp/newinsp/
    return render(request, 'home.html')

def inspecao_id(request):
    #../insp/newinsp/
    return render(request, 'id_input.html')

def edit_insp(request):
    relatorios = Inspection.objects.all().values_list('Ref_Relatorio', flat=True)
    contexto = {"relatorios_id": relatorios}
    return render(request, 'select_edit.html', contexto)


