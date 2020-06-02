from django.urls import path 
#OBSOLETO: from django.contrib import auth 
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import path
from simplemooc.accounts import views 

app_name = 'accounts'
"""
OBSOLETO:
urlpatterns = [ 
	path('entrar', auth.views.login, 
    {'template_name': 'accounts/login.html'}, name='login'),
]
"""
urlpatterns = [ 
    path('', views.dashboard, name='dashboard'),
	path('entrar/', LoginView.as_view(template_name='accounts/login.html'), 
         name='login'),
    path('sair/', LogoutView.as_view(next_page='core:home'), 
         name='logout'),
    path('cadastre-se/', views.register, name='register'),     
    path('editar/', views.edit, name='edit'),     
]