from django.shortcuts import render
from .models import Atleta, Sensei, Evento

def home(request):
    # Buscando dados
    senseis = Sensei.objects.all()
    eventos = Evento.objects.all().order_by('data') # Ordena por data
    
    # Separando atletas
    atletas_destaque = Atleta.objects.filter(destaque=True)
    outros_atletas = Atleta.objects.filter(destaque=False)

    context = {
        'senseis': senseis,
        'atletas_destaque': atletas_destaque,
        'outros_atletas': outros_atletas,
        'eventos': eventos,
    }
    
    return render(request, 'index.html', context)