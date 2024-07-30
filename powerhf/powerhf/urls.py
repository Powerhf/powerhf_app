
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from app.views import *

urlpatterns = [
    # Admin:
    path('admin/', admin.site.urls),

    # Login:
    path('accounts/authentications/', UserLogin, name='auth'),
    path('accounts/registration/', Userregistation, name='register'),
    
    # app folder:
    path('', include('app.urls')),
    path('api/', include('app.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)