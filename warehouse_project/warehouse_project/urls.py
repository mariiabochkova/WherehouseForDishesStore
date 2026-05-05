from django.contrib import admin
from django.urls import path, include  # Додайте include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls')),  # Підключаємо всі адреси з нашого додатку
]