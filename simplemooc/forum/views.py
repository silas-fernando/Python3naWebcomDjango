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
    # Limita a quantidade de tópicos por página.
    paginate_by = 2
    template_name = 'forum/index.html'

    def get_queryset(self):
        queryset = Thread.objects.all()
        order = self.request.GET.get('order', '')  # Recupera o parâmetro GET.
        if order == 'views':  # se for views ordena por views.
            queryset = queryset.order_by('-views')
        elif order == 'answers':  # Se for answers ordena por answers.
            queryset = queryset.order_by('-answers')
        # self.args acessa os parâmetros não nomeados da url e self.kwargs os nomeados.
        tag = self.kwargs.get('tag', '')
        if tag:
            # Filtra as tags que o slug contém.
            queryset = queryset.filter(tags__slug__icontains=tag)
        return queryset

    # Busca todos as variáveis de contexto do template.
    def get_context_data(self, **kwargs):
        context = super(ForumView, self).get_context_data(**kwargs)
        context['tags'] = Thread.tags.all()  # Adiciona as tags ao contexto.
        return context


# as_view() Transforma a classe ForumView em uma função que pode ser usada como uma view.
index = ForumView.as_view()
