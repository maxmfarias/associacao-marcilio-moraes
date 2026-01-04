from django.db import models
from datetime import date
from cloudinary_storage.storage import MediaCloudinaryStorage

class Sensei(models.Model):
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100, help_text="Ex: Mestre Principal, Instrutor")
    graduacao = models.CharField(max_length=100, help_text="Ex: Kodansha 6º Dan")
    
    # ✅ Alterado: Adicionado storage=MediaCloudinaryStorage()
    foto = models.ImageField(upload_to='senseis/', storage=MediaCloudinaryStorage())
    
    biografia = models.TextField()
    anos_experiencia = models.IntegerField(default=0)
    # Para as tags (ex: "Competição, Newaza"), vamos usar um texto simples separado por vírgula
    especialidades = models.CharField(max_length=255, help_text="Separe por vírgula. Ex: Kata, Newaza")

    def __str__(self):
        return self.nome

class Atleta(models.Model):
    nome = models.CharField(max_length=100)
    
    # ✅ Alterado: Adicionado storage=MediaCloudinaryStorage()
    foto = models.ImageField(upload_to='atletas/', storage=MediaCloudinaryStorage(), blank=True, null=True)
    
    destaque = models.BooleanField(default=False, help_text="Se marcado, aparece no carrossel principal.")
    
    # --- MUDANÇA AQUI: Trocamos 'idade' fixa por Data de Nascimento ---
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    
    peso = models.CharField(max_length=20, help_text="Ex: 73kg")
    categoria = models.CharField(max_length=50, help_text="Ex: Juvenil, Sênior")
    graduacao = models.CharField(max_length=50, help_text="Ex: Faixa Preta 1º Dan")
    
    # Adicionei blank=True e null=True para não dar erro se deixar vazio
    principais_conquistas = models.TextField(help_text="Uma conquista por linha", blank=True, null=True)

    # --- LÓGICA DA IDADE AUTOMÁTICA ---
    @property
    def idade(self):
        """Calcula a idade automaticamente baseada no nascimento."""
        if self.data_nascimento:
            today = date.today()
            # Retorna a diferença de anos, ajustando se o aniversário ainda não ocorreu este ano
            return today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))
        return 0

    def __str__(self):
        return self.nome
    
    #Adicionando cor das faixas
    @property
    def cor_faixa(self):
        """Retorna o código HEX da cor baseado no texto da graduação."""
        texto = self.graduacao.lower() # Converte para minúsculo para facilitar a busca
        
        # Dicionário de cores (Você pode ajustar os tons HEX como quiser)
        if 'branca' in texto: return '#FFFFFF'
        if 'cinza' in texto: return '#BEBEBE'
        if 'azul' in texto: return '#007bff' # Azul Bootstrap
        if 'amarela' in texto: return '#FFD700'
        if 'laranja' in texto: return '#FFA500'
        if 'verde' in texto: return '#28a745' # Verde Bootstrap
        if 'roxa' in texto: return '#800080'
        if 'marrom' in texto: return '#8B4513' # SaddleBrown
        if 'preta' in texto: return '#000000'
        if 'coral' in texto: return '#FF7F50'
        if 'vermelha' in texto: return '#dc3545' # Vermelho Bootstrap
        
        return '#ddd' # Cinza claro padrão se não achar nenhuma cor

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
    
    # ✅ Alterado: Adicionado storage=MediaCloudinaryStorage()
    imagem_capa = models.ImageField(upload_to='eventos/', storage=MediaCloudinaryStorage(), blank=True, null=True)
    
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