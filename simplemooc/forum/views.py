from django.shortcuts import render
from django.views.generic import TemplateView


class ForumView(TemplateView):

    template_name = 'forum/index.html'


# as_view() Transforma a classe ForumView em uma função que pode ser usada como uma view.
index = ForumView.as_view()

# index = TemplateView.as_view(template_name='forum/index.html')
