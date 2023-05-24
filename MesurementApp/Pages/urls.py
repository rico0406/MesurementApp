# from django.contrib import admin
from django.urls import path
from . import views
# from .views import UserAutocomplete

urlpatterns = [
    path('', views.home_view, name='home'),
    path('insp_id/', views.inspecao_id, name='insp_id'),
    path('edit/', views.edit_insp, name='edit_insp'),


    # ajax
    # path('ajax/load_users/', views.load_user, name='ajax_load_users'),

    #auto-complete
    # path(
    #     r'^dal/user-autocomplete/$',
    #     UserAutocomplete.as_view(),
    #     name='dal_load_users',
    # ),


]