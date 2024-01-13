from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth
from .utils import validar_senha, validar_tamanho_campos, criar_usuario_banco

# Create your views here.


def login(request):
    if request.method == 'GET':
        return render(request, 'usuarios/login.html')

    if request.method == 'POST':
        user = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(username=user, password=senha)

        if not user:
            messages.add_message(request, constants.ERROR,
                                 'Usuário ou Senha incorretos')
            return redirect('/usuarios/login')

        if user:
            auth.login(request, user)
            return redirect('/eventos/novo_evento/')


def logout(request):
    if request.method == 'GET':
        auth.logout(request)
        return redirect('/usuarios/login')


def cadastro(request):
    if request.method == 'GET':
        return render(request, 'usuarios/cadastro.html')

    elif request.method == 'POST':
        # campos do model User
        usuario = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        # campos do model UserProfile
        nome_completo = request.POST.get('nome_completo')
        telefone = request.POST.get('telefone')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')

        # valida tamanho dos campos
        if not validar_tamanho_campos(request, usuario, email,
                                    nome_completo,telefone, cidade, estado):
            return redirect('/usuarios/cadastro')
        
        
        if not validar_senha(request, senha, confirmar_senha):
            return redirect('/usuarios/cadastro')

        # cria o usuario
        criar_usuario_banco(request, usuario, email, senha,
                                  nome_completo, telefone, cidade, estado)
        
        return redirect('/usuarios/cadastro')
    