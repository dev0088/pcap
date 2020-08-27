"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf.urls.static import static, serve
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_swagger.views import get_swagger_view
from rest_framework import permissions
from rest_framework.authtoken import views

swagger_schema_view = get_swagger_view(title='PCAP API')

schema_view = get_schema_view(
   openapi.Info(
      title="PCAP API",
      default_version='v1',
      description="REST API for PCAP web application",
      terms_of_service="https://google.com/",
      contact=openapi.Contact(email="admin@email.com"),
      license=openapi.License(name="www.pcap.com"),
   ),
   # validators=['flex', 'ssv'],
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # API urls
    url(r'^apis(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^apis/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^api-docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^api-token-auth/', views.obtain_auth_token),
    # Authentication urls
    url(r'^api/v1/auth/', include('authentication.urls')),
    url(r'^api/v1/domain/', include('domain.urls')),
     url(r'^api/v1/http_header_description/', include('http_header_description.urls')),
     url(r'^api/v1/http_header_value_description/', include('http_header_value_description.urls')),
    # Admin URL
    path('admin/', admin.site.urls),
]
