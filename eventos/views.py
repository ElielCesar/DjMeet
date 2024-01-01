from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/usuarios/login')
def novo_evento(request):
    if request.method == 'GET':
        return render(request, 'novo_evento.html')
    
    if request.method == 'POST':
        pass


