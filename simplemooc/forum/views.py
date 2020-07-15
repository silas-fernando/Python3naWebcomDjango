import json

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (TemplateView, View, ListView, DetailView)
from django.contrib import messages
from django.http import HttpResponse

from .models import Thread, Reply
from .forms import ReplyForm


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
        context['tags'] = Thread.tags.all()
        return context


class ThreadView(DetailView):

    model = Thread
    template_name = 'forum/thread.html'

    def get(self, request, *args, **kwargs):
        response = super(ThreadView, self).get(request, *args, **kwargs)
        # Se o usuário não estiver logado ou se ele não for o autor do tópico em questão.
        if not self.request.user.is_authenticated or self.object.author != self.request.user:
            # Conta uma visualização para aquele tópico.
            self.object.views = self.object.views + 1
            self.object.save()
        return response

    def get_context_data(self, **kwargs):
        context = super(ThreadView, self).get_context_data(**kwargs)
        context['tags'] = Thread.tags.all()
        context['form'] = ReplyForm(self.request.POST or None)
        return context

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:  # Se o usuário não estiver logado.
            messages.error(
                self.request, 'Para responder ao tópico é necessário estar logado.'
            )
            return redirect(self.request.path)  # Permanece na mesma página.
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        form = context['form']
        if form.is_valid():
            # Preenche o formulário, mas não o salva.
            reply = form.save(commit=False)
            reply.thread = self.object
            reply.author = self.request.user
            reply.save()
            messages.success(
                self.request, 'A sua resposta foi enviada com sucesso.'
            )
            context['form'] = ReplyForm()  # Limpa o formulário
        # render_to_response: parecido com a função render, mas essa só precisa do contexto.
        return self.render_to_response(context)


class ReplyCorrectView(View):

    correct = True

    def get(self, request, pk):
        reply = get_object_or_404(Reply, pk=pk, thread__author=request.user)
        reply.correct = self.correct
        reply.save()
        message = 'Resposta atualizada com sucesso.'
        if request.is_ajax():
            data = {'Success': True, 'message': message}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            messages.success(request, message)
            return redirect(reply.thread.get_absolute_url())


# as_view() Transforma a classe ForumView em uma função que pode ser usada como uma view.
index = ForumView.as_view()
thread = ThreadView.as_view()
reply_correct = ReplyCorrectView.as_view()
reply_incorrect = ReplyCorrectView.as_view(correct=False)
