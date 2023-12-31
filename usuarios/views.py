from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth

# Create your views here.


def login(request):
    if request.method == 'GET':
        return render(request, 'login/login.html')
    
    if request.method == 'POST':
        user = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(username=user, password=senha)

        if not user:
            messages.add_message(request, constants.ERROR, 'Usuário não existe no sistema')
            return redirect('/usuarios/login')
        
        if user:
            auth.login(request, user)
            return redirect('/eventos/novo_evento/')
            


def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro/cadastro.html')

    elif request.method == 'POST':
        usuario = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        # valida se senhas são iguais
        if not senha == confirmar_senha:
            messages.add_message(request, constants.WARNING, 'as senhas digitadas não são iguais')
            return redirect('/usuarios/cadastro')

        # TODO: Criar funcao usando regex em um arquivo separado para validar forca da senha

        # verifica se o usuario já existe
        user = User.objects.filter(username=usuario)

        if user.exists():
            messages.add_message(request, constants.WARNING, 'O usuário já existe')
            return redirect('/usuarios/cadastro')

        # se não existir, cria o usuario
        if not user.exists():
            user = User.objects.create_user(
                username=usuario, email=email, password=senha)

            messages.add_message(request, constants.SUCCESS, 'Usuário criado com sucesso!')
            return redirect('/usuarios/cadastro')