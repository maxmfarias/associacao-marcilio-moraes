from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views  # Certifique-se que o nome da pasta é 'core'

urlpatterns = [
    path('admin/', admin.site.urls),  # <--- ESSA LINHA É A QUE FALTA
    path('', views.home, name='home'),
]

# Configuração de media para aparecer as fotos
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)