from django.urls import path
from .views import *

urlpatterns = [
    path('novo_evento/', novo_evento, name='novo_evento'),
    path('gerenciar_evento/', gerenciar_evento, name='gerenciar_evento'),
    path('inscrever_evento/<int:id>/', inscrever_evento, name='inscrever_evento'),
    path('participantes_evento/<int:id>', participantes_evento, name='participantes_evento'),
    path('gerar_csv/<int:id>/', gerar_csv, name='gerar_csv'),
]