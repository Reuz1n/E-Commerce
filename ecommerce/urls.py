
from django.contrib import admin
from django.urls import path, include
from store.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls', namespace='store')),  # ¡ojo con el namespace!
]   