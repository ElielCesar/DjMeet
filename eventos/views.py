from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Evento
from django.contrib import messages
from django.contrib.messages import constants
# libs para gerar csv
import csv


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


@login_required(login_url='/usuarios/login')
def gerenciar_evento(request):
    if request.method == 'GET':
        titulo = request.GET.get('nome')
        eventos = Evento.objects.filter(criador=request.user)

        if titulo:
            eventos = eventos.filter(nome__contains=titulo)

        return render(request, 'gerenciar_evento.html', {'eventos': eventos})


@login_required(login_url='/usuarios/login')
def inscrever_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == 'GET':
        return render(request, 'inscrever_evento.html', {'evento': evento})

    elif request.method == 'POST':
        # TODO: validar no backend se o usuário já é um participante
        evento.participantes.add(request.user)
        evento.save()

        messages.add_message(request, constants.SUCCESS,
                             'Inscricao realizada com sucesso!')
        return redirect(f'/eventos/inscrever_evento/{evento.id}/')


def participantes_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == 'GET':
        if evento.criador == request.user:
            participantes = evento.participantes.all()
            return render(request, 'participantes_evento.html', {'participantes': participantes, 'evento': evento})
        else:
            messages.add_message(request, constants.ERROR,
                                 'Esse evento não é seu.')
            return render(request, 'gerenciar_evento.html')


def gerar_csv(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == 'GET':
        if not evento.criador == request.user:
            messages.add_message(request, constants.ERROR,
                                 'Esse evento não é seu.')
            return render(request, 'gerenciar_evento.html')

        participantes = evento.participantes.values_list('username', 'email')
        resposta = HttpResponse(content_type='text/csv')
        resposta['Content-Disposition'] = 'attachment; filename="participantes.csv"'

        escritor = csv.writer(resposta)
        [escritor.writerow(participante) for participante in participantes]
            
        return resposta
