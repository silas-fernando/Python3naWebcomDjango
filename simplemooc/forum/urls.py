from django.urls import path
from simplemooc.forum import views

app_name = 'forum'
urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:tag>/', views.index, name='index_tagged'),
    # Sem o tópico antes do slug, não estava funcionando.
    path('topico/<slug:slug>/', views.thread, name='thread'),
]
