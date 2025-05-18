from rest_framework.schemas import get_schema_view
from django.urls import path

urlpatterns = [
    path('docs/', get_schema_view(
        title="API Documentation",
        description="Your API description",
        version="1.0.0",
        public=True,
    ), name='openapi-schema'),
]
