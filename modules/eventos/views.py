from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Evento, Certificado
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.messages import constants
# libs para gerar csv
import csv

# libs para gerar certificados
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
from django.core.files import File
from django.core.files.base import ContentFile
from io import BytesIO
import os
import random
import string


@login_required(login_url='/usuarios/login')
def novo_evento(request):
    if request.method == 'GET':
        return render(request, 'eventos/novo_evento.html')

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
        
        if len(nome) < 5 or len(descricao) < 5:
            messages.add_message(request, constants.WARNING, 'Os campos nome e descricão devem ter no mínimo 5 caracteres.')
            return redirect('/eventos/novo_evento')
        
        if len(data_inicio) < 8 or len(data_fim) < 8:
            messages.add_message(request, constants.WARNING, 'Valor icorreto nos campos de data')
            return redirect('/eventos/novo_evento')
        
        if data_inicio == None or data_fim == None:
            messages.add_message(request, constants.WARNING, 'Valor icorreto nos campos de data')
            return redirect('/eventos/novo_evento')
        
        if carga_horaria == None or len(str(carga_horaria)) < 1 or int(carga_horaria) < 1:
            messages.add_message(request, constants.WARNING, 'A carga horária tem que ser maior que 0')
            return redirect('/eventos/novo_evento')

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
        # filtros são GET não POST.
        titulo = request.GET.get('nome')
        eventos = Evento.objects.filter(criador=request.user)

        if titulo:
            eventos = eventos.filter(nome__contains=titulo)

        return render(request, 'eventos/gerenciar_evento.html', {'eventos': eventos})


@login_required(login_url='/usuarios/login')
def inscrever_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == 'GET':
        return render(request, 'eventos/inscrever_evento.html', {'evento': evento})

    elif request.method == 'POST':
        evento.participantes.add(request.user)
        evento.save()

        messages.add_message(request, constants.SUCCESS,
                             'Inscricao realizada com sucesso!')
        return redirect(f'/eventos/inscrever_evento/{evento.id}/')


def participantes_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    user = User.objects.all()
    if request.method == 'GET':
        if evento.criador == request.user:
            participantes = evento.participantes.all()
            return render(request, 'eventos/participantes_evento.html',
                          {'participantes': participantes, 'evento': evento, 'user': user})
        else:
            messages.add_message(request, constants.ERROR,
                                 'Esse evento não é seu.')
            return redirect('/eventos/gerenciar_evento/')


@login_required(login_url='/usuarios/login')
def meus_eventos(request):
    eventos = Evento.objects.filter(participantes=request.user)
    return render(request, 'eventos/meus_eventos.html', {'eventos': eventos})


@login_required(login_url='/usuarios/login')
def gerar_csv(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == 'GET':
        participantes = evento.participantes.values_list('userprofile__nome_completo',
                                                         'email', 'userprofile__telefone',
                                                         'userprofile__cidade', 'userprofile__estado')
        resposta = HttpResponse(content_type='text/csv')
        resposta['Content-Disposition'] = 'attachment; filename="participantes.csv"'

        escritor = csv.writer(resposta)
        escritor.writerow(['Nome', 'Email', 'Telefone', 'Cidade', 'Estado'])
        [escritor.writerow(participante) for participante in participantes]
        return resposta


def certificados_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    participantes_usernames = [username for username,
                               in evento.participantes.values_list('username')]

    if request.user != evento.criador and request.user.username not in participantes_usernames:
        messages.add_message(request, constants.WARNING,
                             'Você não se inscreveu nesse evento!')
        return redirect('participantes_evento', id=id)

    # visivel para o criador do evento
    if request.method == "GET" :
        qtd_certificados = evento.participantes.all().count(
        ) - Certificado.objects.filter(evento=evento).count()
        return render(request, 'eventos/certificados_evento.html', {'evento': evento, 'qtd_certificados': qtd_certificados})

# gerador de id randomico para o certificado
def gerar_id(tamanho=10):
    caracteres = string.ascii_lowercase + string.digits
    return ''.join(random.choice(caracteres) for _ in range(tamanho))


@login_required(login_url='/usuarios/login')
def gerar_certificado(request, id):
    evento = get_object_or_404(Evento, id=id)

    if request.user != evento.criador:
        messages.add_message(request, constants.WARNING,'Você não ter permissão para acessar esse evento!')
        return redirect(f'/eventos/certificados_evento/{id}')


    for participante in evento.participantes.all():
        # Evita criar certificados duplicados
        certificado_atual, created = Certificado.objects.get_or_create(
            participante=participante,
            evento=evento,
            defaults={'certificado_id': gerar_id()}
        )
        
        if created:
            '''Carrega modelo do certificado'''
            modelo_certificado_path = os.path.join(settings.MEDIA_ROOT, 'certificados', 'modelo_certificado.png')
            certificado_imagem = Image.open(modelo_certificado_path).convert("RGBA")
            draw = ImageDraw.Draw(certificado_imagem)

            font_path = os.path.join(settings.MEDIA_ROOT, 'fonts', 'arimo.ttf')
            font = ImageFont.truetype(font_path, size=50)

            nome_completo = participante.userprofile.nome_completo
            
            # coordenadas onde o texto será inserido
            draw.text((362, 315), nome_completo, fill="white", font=font)
            font = ImageFont.truetype(font_path, size=20)
            
            draw.text((518, 418), evento.nome, fill="white", font=font)
            
            #draw.text((362, 315), evento.nome, fill="white", font=font)
            draw.text((430, 471), 
                      evento.data_inicio.strftime("%d/%m/%Y") + ' a ' + evento.data_fim.strftime("%d/%m/%Y"),
                      fill="white", font=font)
            
            draw.text((553, 520), str(evento.carga_horaria)+' Horas',fill="white", font=font)
            draw.text((710, 793), certificado_atual.certificado_id, fill="white", font=font)
        
            temp_file = BytesIO()
            certificado_imagem.save(temp_file, format='PNG')
            temp_file.seek(0)
            
             # Atualiza o objeto Certificado com a imagem criada
            certificado_atual.certificado.save(f'certificado_{evento.id}_{participante.id}.png',
                                               ContentFile(temp_file.getvalue()))
            certificado_atual.save()
        
    messages.add_message(request, constants.SUCCESS,'Certificados Gerados com sucesso!')
    return redirect(f'/eventos/certificados_evento/{id}')


@login_required(login_url='/usuarios/login')
def procurar_certificado(request, id):
    evento = get_object_or_404(Evento, id=id)
    
    if request.user != evento.criador:
        messages.add_message(request, constants.WARNING,'Acesse seus certificados pelo menu Participantes > Meus Certificados')
        return redirect('gerenciar_evento')
    
    email = request.POST.get('email')
    certificado = Certificado.objects.filter(evento=evento).filter(participante__email=email).first()
    
    if not certificado:
        messages.add_message(request, constants.WARNING, 'Certificado não encontrado!')
        return redirect(f'/eventos/certificados_evento/{id}')
    
    return redirect(certificado.certificado.url)

@login_required(login_url='/usuarios/login')
def meus_certificados(request):
    certificados = Certificado.objects.filter(participante=request.user)
    return render(request, 'eventos/meus_certificados.html', {'certificados':certificados})


# Esta view deve ser pública para que o certificado seja validado
def validar_certificado(request):
    
    if request.method == 'GET':
        return render(request, 'eventos/validar_certificado.html')
    

    if request.method == 'POST':
        cert_id = request.POST.get('cert_id')
        certificado = Certificado.objects.filter(certificado_id=cert_id).first()
        
        if not certificado:
            messages.add_message(request, constants.WARNING, 'Certificado não encontrado!')
            return redirect('validar_certificado')
        
        return redirect(certificado.certificado.url)
   
    
@login_required(login_url='/usuarios/login')
def deletar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    
    # condicional de seguranca
    if request.user != evento.criador:
        messages.add_message(request, constants.SUCCESS, 'Esse evento não é seu.')
        return redirect('gerenciar_evento')
    
    if request.method == 'GET':
            evento.delete()
            messages.add_message(request, constants.SUCCESS, 'Evento deletado com sucesso')
            return redirect('gerenciar_evento')
        
    return redirect('gerenciar_evento')

@login_required(login_url='/usuarios/login')
def editar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    
    # condicional de seguranca - deve ficar no topo
    if request.user != evento.criador:
        messages.add_message(request, constants.ERROR, 'Esse evento não é seu.')
        return redirect('gerenciar_evento')
    
    if request.method == 'GET':
        return render(request, 'eventos/editar_evento.html', {'evento':evento})
        
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

        # Atualizar os campos do evento
        evento.nome = nome
        evento.descricao = descricao
        evento.data_inicio = data_inicio
        evento.data_fim = data_fim
        evento.carga_horaria = carga_horaria
        evento.logo = logo_evento
        evento.cor_principal = cor_principal
        evento.cor_secundaria = cor_secundaria
        evento.cor_fundo = cor_fundo
        
        evento.save()
        messages.add_message(request, constants.SUCCESS, 'Evento atualizado com sucesso!')
        return redirect('gerenciar_evento')