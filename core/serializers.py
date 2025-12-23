from rest_framework import serializers
from .models import Sensei, Atleta, Evento, Contato

# Serializer do Sensei
class SenseiSerializer(serializers.ModelSerializer):
    # Campo extra para transformar a string "Kata, Newaza" em uma lista ["Kata", "Newaza"]
    lista_especialidades = serializers.SerializerMethodField()

    class Meta:
        model = Sensei
        fields = '__all__' # Pega todos os campos do Model

    def get_lista_especialidades(self, obj):
        if obj.especialidades:
            return [x.strip() for x in obj.especialidades.split(',')]
        return []

# Serializer do Atleta
class AtletaSerializer(serializers.ModelSerializer):
    lista_conquistas = serializers.SerializerMethodField()

    class Meta:
        model = Atleta
        fields = '__all__'

    def get_lista_conquistas(self, obj):
        if obj.principais_conquistas:
            # Quebra o texto onde tiver "Enter" (\n)
            return [x.strip() for x in obj.principais_conquistas.split('\n') if x.strip()]
        return []

# Serializer de Eventos
class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'

# Serializer de Contato
class ContatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contato
        fields = '__all__'