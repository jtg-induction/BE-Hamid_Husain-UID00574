from django.urls import include, path
from django.contrib import admin
from rest_framework.authtoken import views

api_urls = [
    path('todos/', include('todos.urls')),
    path('', include('users.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
]
