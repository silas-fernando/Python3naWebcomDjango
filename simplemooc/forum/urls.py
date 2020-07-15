from django.urls import path
from simplemooc.forum import views

app_name = 'forum'
urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:tag>/', views.index, name='index_tagged'),
    path('respostas/<int:pk>/correta/',
         views.reply_correct, name='reply_correct'),
    path('respostas/<int:pk>/incorreta/',
         views.reply_incorrect, name='reply_incorrect'),
    # Sem o tópico antes do slug, não estava funcionando.
    path('topico/<slug:slug>/', views.thread, name='thread'),
]
