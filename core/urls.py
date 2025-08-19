from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# ----------------------------
# Swagger / OpenAPI
# ----------------------------
schema_view = get_schema_view(
    openapi.Info(
        title="API Gestion taches",
        default_version='v1',
        description="API Pour La Gestion De taches",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="Licence BSD"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# ----------------------------
# Vue racine
# ----------------------------
def redirect_root(request):
    """Redirige la racine vers Swagger UI"""
    return redirect('schema-swagger-ui')

# ----------------------------
# URL patterns
# ----------------------------
urlpatterns = [
    path("", redirect_root),  # racine redirigée vers Swagger
    path("admin/", admin.site.urls),
    path("api/", include("taches.urls")),  # toutes les routes de l'app taches

    # Swagger / ReDoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # DRF Spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
