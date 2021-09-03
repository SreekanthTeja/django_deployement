
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')
urlpatterns = [
    path('swagger',schema_view,  name="docs"),
    path('admin/', admin.site.urls),
    path('',TemplateView.as_view(template_name = 'base.html'), name = 'base-page'),
    path('accounts/', include('accounts.urls')),
    path('buildcron/', include('buildcorn.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

