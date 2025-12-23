from django.db import models

class Sensei(models.Model):
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100, help_text="Ex: Mestre Principal, Instrutor")
    graduacao = models.CharField(max_length=100, help_text="Ex: Kodansha 6º Dan")
    foto = models.ImageField(upload_to='senseis/')
    biografia = models.TextField()
    anos_experiencia = models.IntegerField(default=0)
    # Para as tags (ex: "Competição, Newaza"), vamos usar um texto simples separado por vírgula
    especialidades = models.CharField(max_length=255, help_text="Separe por vírgula. Ex: Kata, Newaza")

    def __str__(self):
        return self.nome

class Atleta(models.Model):
    nome = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='atletas/', blank=True, null=True)
    destaque = models.BooleanField(default=False, help_text="Se marcado, aparece no carrossel principal.")
    idade = models.IntegerField()
    peso = models.CharField(max_length=20, help_text="Ex: 73kg")
    categoria = models.CharField(max_length=50, help_text="Ex: Juvenil, Sênior")
    graduacao = models.CharField(max_length=50, help_text="Ex: Faixa Preta 1º Dan")
    
    # Armazena as conquistas como texto. No frontend, você quebra as linhas.
    principais_conquistas = models.TextField(help_text="Uma conquista por linha")

    def __str__(self):
        return self.nome

class Evento(models.Model):
    TIPO_CHOICES = [
        ('competicao', 'Competição'),
        ('seminario', 'Seminário'),
        ('interno', 'Interno'),
    ]
    
    titulo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    data = models.DateField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    local = models.CharField(max_length=200)
    descricao = models.TextField()
    imagem_capa = models.ImageField(upload_to='eventos/', blank=True, null=True)
    link_info = models.URLField(blank=True, null=True, help_text="Link para 'Saiba mais'")

    class Meta:
        ordering = ['data'] # Ordena sempre pelo mais próximo

    def __str__(self):
        return f"{self.titulo} - {self.data}"

class Contato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True)
    assunto = models.CharField(max_length=100)
    mensagem = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    lido = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} - {self.assunto}"