from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from usuarios import urls

urlpatterns = [
    path('', include('ecommerce.urls')),
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    #path('usuarios/nova-senha', urls.ResetarSenha.as_view(), name='novasenha'),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
