from django.urls import path 
from simplemooc.courses import views 

app_name = 'courses'
urlpatterns = [ 
	path('', views.index, name='index'),
	# path('<int:pk>/', views.details, name='details'),
	path('<slug:slug>/', views.details, name='details'),
]