from django.shortcuts import render, HttpResponse

# Create your views here.


def login(request):
    return render(request, 'login/login.html')


def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro/cadastro.html')
    
    elif request.method == 'POST':
        usuario = request.POST.get('username')
        senha = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        
