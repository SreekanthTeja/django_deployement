from django.urls import path
from blogs import views
from django.views.generic import TemplateView
urlpatterns = [
    path('blog',views.blog, name = 'blog'),
    path('list',views.lead_list, name = 'lead-list'),
    path('detail/<slug:slug>',views.lead_detail, name = 'lead-details'),
    # path('practice',TemplateView.as_view(template_name = 'header.html'), name = 'header-page'),
]