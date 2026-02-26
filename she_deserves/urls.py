from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts1 import views as account_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # SERVER START AVVAGANE DIRECT GA LOGIN PAGE RAVALANTE IDHI PAINA UNDALI
    path('', account_views.login_view, name='root_login'), 
    
    # Migatha app routes ikkada untayi
    path('accounts/', include('accounts1.urls')),
    path('travel/', include('travel.urls')),
]

# Static and Media files (Images) work avvadaniki idhi thappakunda undali
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)