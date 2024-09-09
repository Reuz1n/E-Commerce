
from django.contrib import admin
from django.urls import path, include
from store.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterView.as_view(), name='register'),  # Ruta específica para registro
    path('api/', include('store.urls')),  # Incluye todas las rutas de la app "store"
]
