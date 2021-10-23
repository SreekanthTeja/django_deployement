
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
urlpatterns = [
    path('sheet/apis', TemplateView.as_view(template_name='swagger.html', extra_context={'schema_url':'openapi-schema'}), name='swagger-ui'),
    path('redoc', TemplateView.as_view(template_name='redoc.html', extra_context={'schema_url':'openapi-schema'}), name='redoc'),
    path('openapi', get_schema_view(title="APIs", description="All APIs", version="1.0.0"), name='openapi-schema'),
    path('admin/', admin.site.urls),
    path('',TemplateView.as_view(template_name = 'base.html'), name = 'base-page'),
    path('accounts/', include('accounts.urls')),
    path('buildcron/', include('buildcorn.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

