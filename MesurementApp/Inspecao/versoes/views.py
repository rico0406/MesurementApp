from django.shortcuts import render
from .form import Form_Divisao
from .models import Divisao, Seccao, Inspection
from django.core.cache import cache
from django.contrib.auth.models import User



# def runquery(query):
#     # Build paths inside the project like this: BASE_DIR / 'subdir'.
#     BASE_DIR = Path(__file__).resolve().parent.parent
#     bd = BASE_DIR / 'db.sqlite3'
#     print(bd)
#     # DB Connections
#     conn = pymysql.connect(
#         host=bd,
#         database="db",
#         charset="utf8"
#         # port=33306
#     )
#     # Executa a Query
#     cursor = conn.cursor()
#     cursor.execute(query)



# Create your views here.
def edit_insp(request):

    return render(request, 'edit_insp.html')


def nova_insp(request):
    form = [Form_Divisao()]
    if request.method == "POST":
        idinsp = request.POST['insp_idx']
    newinsp = Inspection.objects.create(Ref_Relatorio=idinsp)

    cache.set('sec', [], 3600)
    contexto = {'forms': form, 'inspecao_id': idinsp, 'n_sec': 1, 'no_div': 1, 'sec_id': 1 }

    return render(request, 'nova_insp.html', contexto)


def download_data(request):

    return render(request, 'download_data.html')


def adiciona_divisao(request):
    no_div = int(request.GET.get('divs'))
    id_insp = int(request.GET.get('insp'))
    id_sec = int(request.GET.get('sec_id'))
    n_sec = int(request.GET.get('n_sec'))
    no_div += 1
    contexto = {}
    formularios = []
    for i in range(no_div):
        form = Form_Divisao()
        # idx = 'form' + str(no_div)
        # formularios[idx] = form
        formularios.append(form)
    print(formularios)
    contexto['forms'] = formularios
    contexto["no_div"] = no_div
    contexto['inspecao_id'] = id_insp
    contexto['sec_id'] = id_sec
    contexto['n_sec'] = n_sec

    print(contexto)
    return render(request, 'adddiv.html', contexto)

def adiciona_bd(request):
    if request.method == "POST":
        post = request.POST.getlist('nome')
        print(post)
        # for i in post:
        #     print(type(post[i]))
    return render(request, 'nova_insp.html')


def adiciona_seccao(request):
    id_sec = int(request.GET.get('sec_id'))
    n_sec = int(request.GET.get('nsec'))
    print(id_sec)

    ls_nome = request.POST.getlist('nome')
    ls_47 = request.POST.getlist('freq47')
    ls_862 = request.POST.getlist('freq862')
    ls_950 = request.POST.getlist('freq950')
    ls_2150 = request.POST.getlist('freq2150')
    data_sec = {"nome": ls_nome, '47': ls_47, '862': ls_862, '950': ls_950, '2150': ls_2150}
    cache.set(id_sec, data_sec, 36000)

    form = [Form_Divisao()]
    id_insp = int(request.GET.get('insp'))

    contexto = {'forms': form, 'inspecao_id': id_insp, 'n_sec': n_sec+1, 'no_div': 1, 'sec_id': n_sec+1}

    return render(request, 'nova_insp.html', contexto)


def cancela_insp(request):
    id_insp = int(request.GET.get('insp'))
    Inspection.objects.get(Ref_Relatorio=id_insp).delete()
    return render(request, 'home.html')

