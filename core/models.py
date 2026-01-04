from django.db import models
from datetime import date
# Importação necessária para o Cloudinary
from cloudinary_storage.storage import MediaCloudinaryStorage

class Sensei(models.Model):
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100, help_text="Ex: Mestre Principal, Instrutor")
    graduacao = models.CharField(max_length=100, help_text="Ex: Kodansha 6º Dan")
    
    foto = models.ImageField(upload_to='senseis/', storage=MediaCloudinaryStorage())
    
    biografia = models.TextField()
    anos_experiencia = models.IntegerField(default=0)
    especialidades = models.CharField(max_length=255, help_text="Separe por vírgula. Ex: Kata, Newaza")

    def __str__(self):
        return self.nome

class Atleta(models.Model):
    nome = models.CharField(max_length=100)
    
    foto = models.ImageField(upload_to='atletas/', storage=MediaCloudinaryStorage(), blank=True, null=True)
    
    destaque = models.BooleanField(default=False, help_text="Se marcado, aparece no carrossel principal.")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    peso = models.CharField(max_length=20, help_text="Ex: 73kg")
    categoria = models.CharField(max_length=50, help_text="Ex: Juvenil, Sênior")
    graduacao = models.CharField(max_length=50, help_text="Ex: Faixa Preta 1º Dan")
    
    principais_conquistas = models.TextField(help_text="Uma conquista por linha", blank=True, null=True)

    # --- LÓGICA DA IDADE ---
    @property
    def idade(self):
        """Calcula a idade automaticamente baseada no nascimento."""
        if self.data_nascimento:
            today = date.today()
            return today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))
        return 0

    # --- LÓGICA DAS CORES DA FAIXA (COM DEGRADÊ) ---
    def _get_cores_detectadas(self):
        """Método auxiliar para achar as cores no texto da graduação."""
        texto = self.graduacao.lower()
        
        # Mapa de cores
        mapa_cores = {
            'branca': '#F5F5F5', # Branco gelo
            'cinza': '#BEBEBE',
            'azul': '#007bff',
            'amarela': '#FFD700',
            'laranja': '#FFA500',
            'verde': '#28a745',
            'roxa': '#800080',
            'marrom': '#8B4513',
            'preta': '#000000',
            'vermelha': '#dc3545',
            'coral': '#FF7F50',
        }
        
        cores_encontradas = []
        # Procura as cores na ordem em que aparecem no texto da graduação
        for nome_cor, hex_code in mapa_cores.items():
            if nome_cor in texto:
                index = texto.find(nome_cor)
                cores_encontradas.append((index, hex_code))
        
        # Ordena pelo índice de aparição
        cores_encontradas.sort(key=lambda x: x[0])
        
        return [c[1] for c in cores_encontradas]

    @property
    def css_faixa(self):
        """Retorna o CSS para o FUNDO do quadradinho (suporta degradê)."""
        cores = self._get_cores_detectadas()
        
        if not cores:
            return '#ddd' # Padrão cinza se não achar nada
            
        if len(cores) >= 2:
            # Cria um gradiente dividido exatamente no meio
            return f"linear-gradient(135deg, {cores[0]} 50%, {cores[1]} 50%)"
            
        return cores[0] # Cor sólida

    @property
    def cor_texto(self):
        """Retorna uma cor sólida para o TEXTO."""
        cores = self._get_cores_detectadas()
        if cores:
            return cores[0]
        return '#666'

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
    
    imagem_capa = models.ImageField(upload_to='eventos/', storage=MediaCloudinaryStorage(), blank=True, null=True)
    
    link_info = models.URLField(blank=True, null=True, help_text="Link para 'Saiba mais'")

    class Meta:
        ordering = ['data']

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