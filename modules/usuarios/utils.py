from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from django.shortcuts import redirect


# valida o tamanho todos os campos de acordo com as regras

def validar_tamanho_campos(request, usuario, email,  nome_completo,
                        telefone, cidade, estado):

        if usuario is None or len(usuario.strip()) < 3:
            messages.add_message(request, constants.WARNING, 'O campo Username precisa de no mínimo 3 caracteres')
            return False
        
        if email is None or len(email.strip()) < 12:
            messages.add_message(request, constants.WARNING, 'O campo Email precisa de no mínimo 12 caracteres')
            return False
        
        if nome_completo is None or len(nome_completo.strip()) < 6:
            messages.add_message(request, constants.WARNING, 'O campo Nome completo precisa de no mínimo 6 caracteres')
            return False
        
        if telefone is None or len(telefone.strip()) < 8:
            messages.add_message(request, constants.WARNING, 'O campo Telefone precisa de no mínimo 8 caracteres')
            return False
        
        if cidade is None or len(cidade.strip()) < 4:
            messages.add_message(request, constants.WARNING, 'O campo Cidade precisa de no mínimo 4 caracteres')
            return False

        if estado is None or len(estado.strip()) < 2:
            messages.add_message(request, constants.WARNING, 'Selecione um estado')
            return False
        
        return True


# regras para validar as senhas

def validar_senha(request, senha, confirmar_senha):
    if senha is None or len(senha.strip()) < 5:
        messages.add_message(request, constants.WARNING,'A senha deve ter no mínimo 5 caracteres')
        return False

    if senha != confirmar_senha:
        messages.add_message(request, constants.WARNING,'As senhas digitadas não são iguais')
        return False
    
    return True


# valida se usuario existe no banco de dados

def criar_usuario_banco(request, usuario, email, senha, nome_completo, telefone, cidade, estado):
        
        if User.objects.filter(username=usuario).exists():
            messages.add_message(request, constants.WARNING, 'Um usuário com esse username já existe!')
            return redirect('/usuarios/cadastro')

        else:
            user = User.objects.create_user(username=usuario, email=email, password=senha)
            UserProfile.objects.create(user=user, nome_completo=nome_completo, telefone=telefone, cidade=cidade, estado=estado)
            messages.add_message(request, constants.SUCCESS,'Usuário criado com sucesso!')
            return redirect('/usuarios/cadastro')
