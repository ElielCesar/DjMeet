from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Evento
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.


@login_required(login_url='/usuarios/login')
def novo_evento(request):
    if request.method == 'GET':
        return render(request, 'novo_evento.html')

    elif request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_termino')
        carga_horaria = request.POST.get('carga_horaria')
        logo_evento = request.FILES.get('logo')
        cor_principal = request.POST.get('cor_principal')
        cor_secundaria = request.POST.get('cor_secundaria')
        cor_fundo = request.POST.get('cor_fundo')

        evento = Evento(
            criador=request.user,
            nome=nome,
            descricao=descricao,
            data_inicio=data_inicio,
            data_fim=data_fim,
            carga_horaria=carga_horaria,
            logo=logo_evento,
            cor_principal=cor_principal,
            cor_secundaria=cor_secundaria,
            cor_fundo=cor_fundo,
        )

        evento.save()

        messages.add_message(request, constants.SUCCESS,
                             'Evento cadastrado com sucesso!!')
        return redirect('/eventos/novo_evento')


def gerenciar_evento(request):
    if request.method == 'GET':
        titulo = request.GET.get('nome')
        eventos = Evento.objects.filter(criador=request.user)

        if titulo:
            eventos = eventos.filter(nome__contains=titulo)
        
        return render(request, 'gerenciar_evento.html', {'eventos': eventos})

def inscrever_evento(request, id):
    # TODO: validar login
    evento = get_object_or_404(Evento, id=id)
    if request.method == 'GET':
        return HttpResponse(evento.nome)
    
