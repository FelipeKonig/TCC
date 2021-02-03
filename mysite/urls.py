from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('apps.ecommerce.urls')),
    path('usuarios/', include('apps.usuarios.urls')),
    path('empresas/', include('apps.empresas.urls')),
    path('vitrines/', include('apps.vitrines.urls')),
    path('produtos/', include('apps.produtos.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
