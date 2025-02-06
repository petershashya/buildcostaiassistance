from django.contrib import admin
from django.urls import include, path
from . import views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('accounts/login/', views.login_view, name='account_login'),
    path('register/', views.register_view, name='register'),
    path('predict/', login_required(views.predict), name='predict'),
    path('history/',login_required(views.history_view), name='history'),
    path('logout/',views.logout_view, name='logout'),
    path('prediction/',views.prediction, name='prediction'),
    path('loader/', views.loader_view, name='loader'),

    #Admin Pages Starts Here
    path('admin-page/',login_required(views.admin_page), name='admin-page'),

    path('admin-users/',login_required(views.admin_users), name='admin-users'),
    path('admin-report/',login_required(views.admin_report), name='admin-report'),
    path('admin-history', login_required(views.historyview), name='admin-history'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)