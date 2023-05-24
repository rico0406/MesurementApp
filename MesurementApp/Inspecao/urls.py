# from django.contrib import admin
from django.urls import path
from . import views
# from .views import UserAutocomplete

urlpatterns = [
    path('newinsp/', views.nova_insp, name='new'),
    path('download/', views.download_data, name='download'),
    path('seleciona_insp/', views.seleciona_inspecao, name='seleciona'),
    # path('send/', views.adiciona_bd, name='envia_dados'),
    path('cancel/', views.cancela_insp, name='cancelar'),
    path('check_input/', views.trata_submit, name='trata_input'),
    path('load/', views.load_insp, name='load'),
    path('del_sec/', views.deleta_seccao, name='deleta_sec'),
    path('input_in/', views.get_in, name='input_in'),
    path('save_in/', views.save_in, name='save_in'),
]


