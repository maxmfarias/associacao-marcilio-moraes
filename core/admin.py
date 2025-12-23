from django.contrib import admin
from .models import Sensei, Atleta, Evento, Contato

 
admin.site.register(Sensei)
admin.site.register(Atleta)
admin.site.register(Evento)
admin.site.register(Contato)