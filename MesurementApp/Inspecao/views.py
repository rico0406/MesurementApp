from django.shortcuts import render, redirect
from .form import Form_Divisao
from .models import Divisao, Seccao, Inspection
from django.core.cache import cache
import pandas as pd
from django.http import HttpResponse
from django.contrib import messages
from io import BytesIO
from django.contrib.auth.models import User



# Create your views here.

NEW_FORM = [
                Form_Divisao(initial={'nome': 'Out'}),
                Form_Divisao(initial={'nome': 'Division A'}),
                Form_Divisao(initial={'nome': 'Division B'}),
                Form_Divisao(initial={'nome': 'Division C'}),
                Form_Divisao(initial={'nome': 'Division D'}),
                Form_Divisao(initial={'nome': 'Division E'}),
            ]


def get_in(request):
    """

    Trata os request para inserir os valores da medição IN. Deve ser feito no inicio da inspeção e tem o campo nome não
    editável. Passa apenas os campos das frequências para o front-end

    """

    if request.method == "POST":
        idinsp = int(request.POST['insp_idx'].replace('-', ''))

        check = Inspection.objects.filter(Ref_Relatorio=idinsp)
        if check:
            messages.add_message(request, messages.INFO,
                                 'ID already registered, please enter a different register number.')
            return render(request, 'id_input.html')

        # Salva o id da inspeção temporariamente na cache para poder ser recuperada e deletada quando se for começar a
        # inspeção. Foi-se feito dessa forma pois save_in usa redirect e ia dar muito trabalho modificar o programa

        cache.set(100, idinsp, 18000)
        form = Form_Divisao(initial={'nome': 'Ref'})
        contexto = {'form': form,
                    'nome': 'Reference'}

    return render(request, 'input_in.html', contexto)

def save_in(request):
    """
    Trata os requests enviados para guardar os valores de IN na memória cache na sec_id = 0. Essa função faz redirect
    para a função nova_insp, onde se inicializará as medições das instalações

    """

    if request.method == 'POST':
        name = request.POST.getlist('nome')
        mp1 = request.POST.getlist('mesurement_point1')
        mp2 = request.POST.getlist('mesurement_point2')
        mp3 = request.POST.getlist('mesurement_point3')
        mp4 = request.POST.getlist('mesurement_point4')

        data_sec = {"nome": name, 'mp1': mp1,
                    'mp2': mp2, 'mp3': mp3,
                    'mp4': mp4, 'name_sec': 'IN'}
        cache.set(0, data_sec, 18000)

    return redirect('new')

def nova_insp(request):
    """
    Trata os request para abrir a página de uma nova inspeção. Inicializa a página com só um form com a divisão
    com o nome 'Out' já que todas as fracções começam com essa divisão.


    """

    # Obtém o id da inspeção e depois deleta do cache

    idinsp = cache.get(100)

    form = NEW_FORM

    no_div = len(form)
    # form = Form_Divisao()

    # newinsp = Inspection.objects.create(Ref_Relatorio=idinsp)

    pags = [1]
    # pags = []
    # cache.set('sec', [], 3600)
    contexto = {'forms': form,
                'inspecao_id': idinsp,
                'n_sec': 1,
                'no_div': no_div,
                'sec_id': 1,
                'sec_name': '1',
                'seccoes': pags}

    return render(request, 'nova_insp.html', contexto)


def seleciona_inspecao(request):
    """
    Trata os request para selecionar os dados a serem descarregados. Junta as inspeções disponíveis e as devolve para
    o front-end

    """

    relatorios = Inspection.objects.all().values_list('Ref_Relatorio', flat=True)
    contexto = {"relatorios_id": relatorios}
    return render(request, 'select_id.html', contexto)


def download_data(request):
    """
    Trata os request para descarregar o ficheiro .csv da base de dados com id 'selected_id'. Busca na base de dados os
    dados associados e realiza os calculos em cima deles. Após isso inicia o download para o útilizador.

    """
    if request.method == 'POST':
        relatorio_id = request.POST.get('selected_id')
        seccoes = Seccao.objects.filter(inspec=relatorio_id)
        divs = Divisao.objects.filter(sec__in=seccoes.values('id'))
        df_sec = pd.DataFrame.from_records(seccoes.values())
        df_div = pd.DataFrame.from_records(divs.values())
        tabela = df_sec.merge(df_div, left_on='id', right_on='sec_id', how='left')
        tabela.drop(['id_x', 'id_y', 'sec_id', 'inspec_id'], axis=1, inplace=True)

        tabela[
            ["mesurement_point1", 'mesurement_point2', 'mesurement_point3', 'mesurement_point4']
        ] = tabela[
            ["mesurement_point1", 'mesurement_point2', 'mesurement_point3', 'mesurement_point4']
        ].astype(float)

        tabela.rename(columns={
            'nome_x': 'Section',
            'nome_y': 'Division',
            "mesurement_point1": "Mesurement Point 1",
            'mesurement_point2': 'Mesurement Point 2',
            'mesurement_point3': 'Mesurement Point 3',
            'mesurement_point4': 'Mesurement Point 4'
        }, inplace=True)

        # tabela.to_csv('C:/Users/rro/IEP/AppTelecom/tabela.csv', index=False, sep=';')

        # Substitui por vazio todos os valores repetidos na Fracção
        # Apaga o 0 na coluna Fracção para que o IN fique sem fracção
        tabela['Section'] = tabela['Section'].replace(0, None)
        # Deixa o nome de cada fração só aparecendo uma vez
        tabela['Section'][tabela.duplicated('Section', keep='first')] = None

        # Primeira linha da tabela será utiizada para fazer a tabela secundária
        df_in = tabela.iloc[0, 2:].copy()

        # Cria tabela secundária
        tabela_diff = tabela.copy().apply(lambda x: x-df_in, axis=1)

        # Retira colunas Divisão e Fracção
        tabela_diff = tabela_diff.drop(['Division', 'Section'], axis=1)

        # Tranforma as colunas das frequencias em float
        tabela_diff = tabela_diff.astype(float)

        # Ordena as colunas e coloca os nomes utilizados no ficheiro excel
        tabela_diff = tabela_diff.reindex(columns=["Mesurement Point 1", 'Mesurement Point 2', 'Mesurement Point 3', 'Mesurement Point 4'])
        tabela_diff.rename(columns={
            "Mesurement Point 1": "AT Mesurement Point 1",
            'Mesurement Point 2': 'AT Mesurement Point 2',
            'Mesurement Point 3': 'AT Mesurement Point 3',
            'Mesurement Point 4': 'AT Mesurement Point 4'},
            inplace=True)

        # Tira o zero da primeira linha e substitui por vazio
        tabela_diff.replace(0, None, inplace=True)

        # Cria o objeto BytesIO
        output = BytesIO()

        # Cria o ExcelWriter
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        print(tabela_diff.columns)
        print(tabela_diff.dtypes)

        # Escreve as tabelas no arquivo Excel
        tabela.to_excel(writer, sheet_name='Sheet1', startrow=0, startcol=0, index=False, float_format='%.2f')
        tabela_diff.to_excel(writer, sheet_name='Sheet1', startrow=0, startcol=7, index=False, float_format='%.2f')

        # Salva o arquivo Excel
        writer.save()

        # Cria a resposta HTTP
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{relatorio_id}.xlsx"'

        # Escreve o conteúdo do BytesIO na resposta HTTP
        output.seek(0)
        response.write(output.getvalue())

        # Retorna a resposta HTTP
        return response

        # Ficheiro para download
        # response = HttpResponse(tabela.to_csv(index=False, encoding='utf-8', sep=';'),
        #                         content_type='text/csv', charset='latin1')
        # response['Content-Disposition'] = f'attachment; filename="{relatorio_id}.csv"'
        # return response

    return redirect('home')


def cancela_insp(request):
    """
    Trata os request para cancelar a inspeção atual e volta para a página inicial.

    """

    # Inspection.objects.get(Ref_Relatorio=id_insp).delete()
    try:
        # id_insp = int(request.GET.get('insp'))
        n_sec = int(request.GET.get('nsec'))
        keys = range(1, n_sec, 1)
        cache.delete_many(keys)
    except Exception as e:
        print(e)

    finally:
        return render(request, 'home.html')


def deleta_seccao(request):
    """
    Trata os request para excluir a secção (fracção) atual. Caso não seja a primeira seccção ela passa para a anterior,
    se for a primeira, passa para a nova primeira.

    """
    id_sec = int(request.GET.get('sec_id'))
    n_sec = int(request.GET.get('nsec'))-1
    id_insp = int(request.GET.get('insp'))

    if id_sec > n_sec:
        cache.delete(id_sec)
        idx = n_sec
    else:
        for i in range(2, n_sec + 2, 1):
            if i > id_sec:
                reg = cache.get(i)
                cache.set(i-1, reg, 18000)
        cache.delete(n_sec+1)
        idx = id_sec

    reg = cache.get(idx)
    divs = len(reg['nome'])
    name_sec = reg['name_sec']
    inicial = {}
    forms = []
    for i in range(divs):
        inicial['nome'] = reg['nome'][i]
        inicial['mesurement_point1'] = reg['mp1'][i]
        inicial['mesurement_point2'] = reg['mp2'][i]
        inicial['mesurement_point3'] = reg['mp3'][i]
        inicial['mesurement_point4'] = reg['mp4'][i]
        forms.append(Form_Divisao(initial=inicial))

    pags = range(1, n_sec + 1, 1)
    contexto = {'forms': forms, 'inspecao_id': id_insp, 'n_sec': n_sec, 'no_div': divs,
                'sec_id': idx, 'sec_name': name_sec, 'seccoes': pags}
    return render(request, 'nova_insp.html', contexto)

def trata_submit(request):

    """
    Trata os request dado pelo submit do form de inspeção. Essa função verifica qual botão foi apertado através do
    request.POST e com isso seleciona a ação desejada.

    add_sec == Adiciona secção(fracção)
    add_div == Adiciona divisão
    del_div == deleta divisão
    send == Guarda as informações na Base de dados
    pag == Seleciona a secção desejada

    """
    # Deleta a posição na cache 100 onde ficou salvo os valores do IN no inicio da inspeção
    # Isso evita que esse valor vá pra algum dos processos subsequentes
    cache.delete(100)

    # Retira as informações passadas por GET
    id_sec = int(request.GET.get('sec_id'))
    n_sec = int(request.GET.get('nsec'))
    id_insp = int(request.GET.get('insp'))
    no_div = int(request.GET.get('divs'))

    # Todas as outras interações vão depender de ter sido feito um envio por POST
    if request.method == 'POST':
        # informações do form da divisão
        ls_nome = request.POST.getlist('nome')
        ls_mp1 = request.POST.getlist('mesurement_point1')
        ls_mp2 = request.POST.getlist('mesurement_point2')
        ls_mp3 = request.POST.getlist('mesurement_point3')
        ls_mp4 = request.POST.getlist('mesurement_point4')

        # Nome da secção (fracção)
        name_sec = request.POST['fraccao']

        if 'add_sec' in request.POST:

            save_sec_cache(ls_nome, ls_mp1, ls_mp2, ls_mp3, ls_mp4, id_sec, name_sec)

            # form = [Form_Divisao(initial={'nome': 'Out'})]
            form = NEW_FORM

            pags = range(1, n_sec + 2, 1)
            new_sec_id = n_sec + 1
            no_div = len(form)

            contexto = {'forms': form, 'inspecao_id': id_insp, 'n_sec': new_sec_id, 'no_div': no_div,
                        'sec_id': new_sec_id, 'sec_name': new_sec_id, 'seccoes': pags}

            return render(request, 'nova_insp.html', contexto)

        elif 'add_div' in request.POST:

            forms = []
            inicial = {}
            for i in range(no_div):
                inicial['nome'] = ls_nome[i]
                inicial['mesurement_point1'] = ls_mp1[i]
                inicial['mesurement_point2'] = ls_mp2[i]
                inicial['mesurement_point3'] = ls_mp3[i]
                inicial['mesurement_point4'] = ls_mp4[i]
                forms.append(Form_Divisao(initial=inicial))

            forms.append(Form_Divisao())
            no_div += 1
            pags = range(1, n_sec+1, 1)
            contexto = {'forms': forms, 'inspecao_id': id_insp, 'n_sec': n_sec, 'no_div': no_div,
                        'sec_id': id_sec, 'sec_name': name_sec, 'seccoes': pags}

            return render(request, 'nova_insp.html', contexto)

        elif 'del_div' in request.POST:
            deletada = int(request.POST['del_div']
)
            forms = []
            inicial = {}

            for i in range(no_div):
                if i != deletada:
                    inicial['nome'] = ls_nome[i]
                    inicial['mesurement_point1'] = ls_mp1[i]
                    inicial['mesurement_point2'] = ls_mp2[i]
                    inicial['mesurement_point3'] = ls_mp3[i]
                    inicial['mesurement_point4'] = ls_mp4[i]
                    forms.append(Form_Divisao(initial=inicial))

            no_div -= 1
            pags = range(1, n_sec + 1, 1)
            contexto = {'forms': forms, 'inspecao_id': id_insp, 'n_sec': n_sec, 'no_div': no_div,
                        'sec_id': id_sec, 'sec_name': name_sec, 'seccoes': pags}

            return render(request, 'nova_insp.html', contexto)

        elif 'send' in request.POST:
            save_sec_cache(ls_nome, ls_mp1, ls_mp2, ls_mp3, ls_mp4, id_sec, name_sec)

            inspecao, _ = Inspection.objects.get_or_create(Ref_Relatorio=id_insp)


            for i in range(0, n_sec+1, 1):

                # Gera um id de secção com o id da secção dentro da inspeção e o id da inspeção
                id_sec_com = 10000*id_insp+i

                # Atribui a reg os valores com id i na memoria cache
                reg = cache.get(i)

                # Verifica se já existe a secção com o index id_sec_com na base de dados para caso de alterações.
                # Caso não exista ela sera criada com o nome e index de inspeção selecionados
                seccao, created = Seccao.objects.get_or_create(id=id_sec_com,
                                                               defaults={'nome': reg['name_sec'], 'inspec': inspecao})

                if not created:
                    divisoes_existentes = Divisao.objects.filter(sec=seccao)
                    divisoes_existentes.delete()
                    Seccao.objects.filter(id=id_sec_com).update(nome=reg['name_sec'])

                for j in range(len(reg['nome'])):
                    Divisao.objects.create(
                        nome=reg['nome'][j],
                        sec=seccao,
                        mesurement_point1=reg['mp1'][j],
                        mesurement_point2=reg['mp2'][j],
                        mesurement_point3=reg['mp3'][j],
                        mesurement_point4=reg['mp4'][j]
                    )

            return redirect('home')

        elif 'pag' in request.POST:
            save_sec_cache(ls_nome, ls_mp1, ls_mp2, ls_mp3, ls_mp4, id_sec, name_sec)
            next_id = request.POST['pag']
            reg = cache.get(next_id)

            # Nome da secção (fracção) selecionada

            name_sec = reg['name_sec']
            divs = len(reg['nome'])
            inicial = {}
            forms = []
            for i in range(divs):
                inicial['nome'] = reg['nome'][i]
                inicial['mesurement_point1'] = reg['mp1'][i]
                inicial['mesurement_point2'] = reg['mp2'][i]
                inicial['mesurement_point3'] = reg['mp3'][i]
                inicial['mesurement_point4'] = reg['mp4'][i]
                forms.append(Form_Divisao(initial=inicial))

            pags = range(1, n_sec + 1, 1)
            contexto = {'forms': forms,
                        'inspecao_id': id_insp,
                        'n_sec': n_sec,
                        'no_div': divs,
                        'sec_id': next_id,
                        'sec_name': name_sec,
                        'seccoes': pags}

            return render(request, 'nova_insp.html', contexto)

    return redirect('home')
# <button formmethod="post" type="submit" name='save' value="save">Salvar</button>
# <a href="{% url 'pag_sec' %}?divs={{no_div}}&insp={{inspecao_id}}&nsec={{n_sec}}&sec_id={{i}}" class="ajusta-link">
#                         {{ i }}
#                     </a>


def load_insp(request):
    """
    Trata os requests do pedido de carregar alguma inspeção existente da BD. Carrega os dados e os envia para a cache,
    como se o programa já estivesse no meio de uma inspeção.

    """
    if request.method == 'POST':
        id_insp = request.POST.get('selected_id')
        seccoes = Seccao.objects.filter(inspec=id_insp)
        n_sec = len(seccoes)-1
        # Número de fracções no local
        # Usa-se o - 2 para não contar a IN.
        # n_sec = len(seccoes) - 2

        id_sec = 1

        cont_sec = 0

        for sec in seccoes:
            sec_id = (getattr(sec, 'id'))
            name_sec = (getattr(sec, 'nome'))
            cache_sec_id = int(sec_id) - 10000*int(id_insp)
            div = Divisao.objects.filter(sec_id=sec_id)
            df_div = pd.DataFrame.from_records(div.values())

            save_sec_cache(df_div['nome'].tolist(), df_div['mesurement_point1'].tolist(),
                           df_div['mesurement_point2'].tolist(), df_div['mesurement_point3'].tolist(),
                           df_div['mesurement_point4'].tolist(), cache_sec_id, name_sec)

            if cont_sec == 1:
                no_div = len(div)
                inicial = {}
                forms = []
                for i in range(len(div)):
                    inicial['nome'] = getattr(div[i], 'nome')
                    inicial['mesurement_point1'] = getattr(div[i], 'mesurement_point1')
                    inicial['mesurement_point2'] = getattr(div[i], 'mesurement_point2')
                    inicial['mesurement_point3'] = getattr(div[i], 'mesurement_point3')
                    inicial['mesurement_point4'] = getattr(div[i], 'mesurement_point4')
                    forms.append(Form_Divisao(initial=inicial))
                    nome_sec_inicial = name_sec
            cont_sec += 1

        pags = range(1, n_sec + 1, 1)

        contexto = {'forms': forms, 'inspecao_id': int(id_insp), 'n_sec': n_sec, 'no_div': no_div,
                    'sec_id': id_sec, 'sec_name': nome_sec_inicial, 'seccoes': pags}

        return render(request, 'nova_insp.html', contexto)





        # response.flush()
        # return redirect('home')

    return render(request, 'nova_insp.html')


def save_sec_cache(ls_nome, ls_mp1, ls_mp2, ls_mp3, ls_mp4, id_sec, name_sec=None):
    """
    Salva os dados de uma secção (fracção) na memoria cache.

    :param ls_nome: Lista de nomes de divisão
    :param ls_mp1: Lista das medidas de Mesurement Point 1 da secção por divisão
    :param ls_mp2: Lista das medidas de Mesurement Point 2 da secção por divisão
    :param ls_mp3: Lista das medidas de Mesurement Point 3 da secção por divisão
    :param ls_mp4: Lista das medidas de Mesurement Point 4 da secção por divisão
    :param id_sec: Index da secção a ser gravada no cache
    :param name_sec: Nome da secção a ser gravada no cache
    """

    if not name_sec:
        name_sec = str(id_sec)

    # Para gravar na cache tem que ser um dicionário.
    # Como pode-se ter mais de um valor associado com cada divisão, os atributos da Divisão são passados por listas
    data_sec = {"nome": ls_nome,
                'mp1': ls_mp1,
                'mp2': ls_mp2,
                'mp3': ls_mp3,
                'mp4': ls_mp4,
                'name_sec': name_sec}

    cache.set(id_sec, data_sec, 18000)
