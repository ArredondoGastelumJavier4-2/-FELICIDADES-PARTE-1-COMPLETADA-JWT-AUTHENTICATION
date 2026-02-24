# ===================================
# URLS DE LA API - libros/api_urls.py
# ===================================

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .jwt_views import CustomTokenObtainPairView
from . import oauth_views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from . import api_views

# ===== ROUTER PARA VIEWSETS =====
router = DefaultRouter()
router.register(r'libros', api_views.LibroViewSet, basename='libro')
router.register(r'autores', api_views.AutorViewSet, basename='autor')
router.register(r'categorias', api_views.CategoriaViewSet, basename='categoria')
router.register(r'prestamos', api_views.PrestamoViewSet, basename='prestamo')

urlpatterns = [
    # ─────────────────────────────────
    # 🔐 AUTENTICACIÓN JWT
    # ─────────────────────────────────
    path('auth/jwt/login/', CustomTokenObtainPairView.as_view(), name='jwt_login'),
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('auth/jwt/verify/', TokenVerifyView.as_view(), name='jwt_verify'),

    # ─────────────────────────────────
    # 🔑 AUTENTICACIÓN OAUTH (GOOGLE)
    # ─────────────────────────────────
    path('auth/google/redirect/', oauth_views.google_oauth_redirect, name='google_redirect'),
    path('auth/google/callback/', oauth_views.google_oauth_callback, name='google_callback'),

    # ─────────────────────────────────
    # 📚 ENDPOINTS CRUD
    # ─────────────────────────────────
    path('', include(router.urls)),
]