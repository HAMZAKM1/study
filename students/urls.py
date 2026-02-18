from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔥 Custom Login (MUST COME BEFORE include)
    path('accounts/login/',
         auth_views.LoginView.as_view(
             template_name='study/login.html'
         ),
         name='login'),

    path('accounts/logout/',
         auth_views.LogoutView.as_view(),
         name='logout'),

    # Other auth URLs (password reset etc.)
    path('accounts/', include('django.contrib.auth.urls')),

    # Your app URLs
    path('', include('study.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
