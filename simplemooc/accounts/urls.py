from django.urls import path 
#OBSOLETO: from django.contrib import auth 
from django.contrib.auth.views import LoginView
from django.urls import path

app_name = 'accounts'
"""
OBSOLETO:
urlpatterns = [ 
	path('entrar', auth.views.login, 
    {'template_name': 'accounts/login.html'}, name='login'),
]
"""
urlpatterns = [ 
	path('entrar/', LoginView.as_view(template_name='accounts/login.html'), 
         name='login'),
]