from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers
from knox import views as knox_views


router = routers.DefaultRouter()
router.register(r'quotes', views.QuoteViewSet, basename='quotes')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    #path('get_quote/', views.get_quote, name='quote'),
    #path('send_sms/', views.send_quote_sms, name='sms'),
    path('api/register/', views.RegisterAPI.as_view(), name='register'),
    path('api/login/', views.LoginAPI.as_view(), name='login'),
    path('api/user/', views.UserAPI.as_view(), name='user'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall')
]



