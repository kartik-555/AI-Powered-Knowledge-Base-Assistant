# filepath: /Users/rdghosh1/Documents/GitHub/AI-Powered-Knowledge-Base-Assistant/knowledgebase/knowledgebase/urls.py
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Knowledge Base Assistant API",
        default_version='v1',
        description="API documentation for the Knowledge Base Assistant",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@knowledgebase.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('assistant.urls')),  # API routing to the 'assistant' app
    # OpenAPI schema generation
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/schema/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]