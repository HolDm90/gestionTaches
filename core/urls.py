from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Redirection racine
def redirect_root(request):
    return redirect('swagger-ui')

urlpatterns = [
    path("", redirect_root),
    path("admin/", admin.site.urls),
    path("api/", include("taches.urls")),

    # DRF Spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
