# assistant/urls.py
from django.urls import path
from .views import QueryView, DocumentUploadView

urlpatterns = [
    path('query/', QueryView.as_view(), name='query-api'), 
    path('upload/', DocumentUploadView.as_view(), name='upload-api'),
]
