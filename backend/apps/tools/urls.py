from django.urls import path
from .views import openapi_spec
from django.views.generic import TemplateView

urlpatterns = [
    path('openapi_spec', openapi_spec, name='openapi_spec'),
    path('docs/', TemplateView.as_view(
        template_name='swagger-ui.html'
    ), name='swagger-ui'),
]
