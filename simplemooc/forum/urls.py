from django.urls import path
from simplemooc.forum import views

app_name = 'forum'
urlpatterns = [
    path('', views.ForumView, name='index'),
]
