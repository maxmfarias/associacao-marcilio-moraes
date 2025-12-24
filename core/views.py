from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Atleta, Sensei, Evento, Contato

def home(request):
    # --- LÓGICA DO FORMULÁRIO (SALVAR DADOS) ---
    if request.method == "POST":
        # Pegando os dados que vieram do HTML (pelo 'name' do input)
        nome_digitado = request.POST.get('name')
        email_digitado = request.POST.get('email')
        mensagem_digitada = request.POST.get('message')
        
        # Salvando no Banco de Dados
        # Obs: Como o form atual não tem 'assunto' nem 'telefone', 
        # vamos salvar com um valor padrão para não dar erro.
        Contato.objects.create(
            nome=nome_digitado,
            email=email_digitado,
            mensagem=mensagem_digitada,
            assunto="Contato pelo Site", 
            telefone="" 
        )
        
        # Mensagem de sucesso para aparecer na tela
        messages.success(request, 'Sua mensagem foi enviada com sucesso!')
        
        # Recarrega a página limpa
        return redirect('home')

    # --- LÓGICA DE EXIBIÇÃO (GET) ---
    senseis = Sensei.objects.all()
    eventos = Evento.objects.all().order_by('data')
    
    atletas_destaque = Atleta.objects.filter(destaque=True)
    outros_atletas = Atleta.objects.filter(destaque=False)

    context = {
        'senseis': senseis,
        'atletas_destaque': atletas_destaque,
        'outros_atletas': outros_atletas,
        'eventos': eventos,
    }
    
    return render(request, 'index.html', context)