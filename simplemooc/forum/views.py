from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView

from .models import Thread


# class ForumView(TemplateView):

#   def get(self, request, *args, **kwargs):
#   return render(request, 'forum/index.html')

# class ForumView(TemplateView):

#   template_name = 'forum/index.html'

# index = TemplateView.as_view(template_name='forum/index.html')

class ForumView(ListView):  # Model para listagem de Tópicos.

    model = Thread
    paginate_by = 10  # Limita a quantidade de itens listados.
    template_name = 'forum/index.html'


# as_view() Transforma a classe ForumView em uma função que pode ser usada como uma view.
index = ForumView.as_view()
