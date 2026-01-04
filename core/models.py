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
        # Ex: "Faixa Azul/Amarela" -> vai achar azul primeiro, depois amarela
        for nome_cor, hex_code in mapa_cores.items():
            if nome_cor in texto:
                # Armazena a posição onde a cor foi achada para ordenar corretamente
                index = texto.find(nome_cor)
                cores_encontradas.append((index, hex_code))
        
        # Ordena pelo índice de aparição (quem aparece primeiro no nome ganha)
        cores_encontradas.sort(key=lambda x: x[0])
        
        return [c[1] for c in cores_encontradas]

    @property
    def css_faixa(self):
        """Retorna o CSS para o FUNDO do quadradinho (suporta degradê)."""
        cores = self._get_cores_detectadas()
        
        if not cores:
            return '#ddd' # Padrão cinza se não achar nada
            
        if len(cores) >= 2:
            # Cria um gradiente dividido exatamente no meio (50%/50%)
            # Ex: Azul na esquerda, Amarela na direita
            return f"linear-gradient(135deg, {cores[0]} 50%, {cores[1]} 50%)"
            
        return cores[0] # Cor sólida

    @property
    def cor_texto(self):
        """Retorna uma cor sólida para o TEXTO (pega a primeira cor da faixa)."""
        cores = self._get_cores_detectadas()
        if cores:
            return cores[0]
        return '#666'

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