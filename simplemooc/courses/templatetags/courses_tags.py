# Usado para criar tags customizadas semelhante a tag static, com o propósito de evitar repetição de código.
from django.template import Library

register = Library()

from simplemooc.courses.models import Enrollment

# Converte a função abaixo em uma tag de fato, que podera ser usada pelo django.
# Quando a tag my_courses for chamada, o template passado como parametro no decorator, será carregado.
@register.inclusion_tag('courses/templatetags/my_courses.html') 
def my_courses(user):
    enrollments = Enrollment.objects.filter(user=user) # Busca todas as inscrições do usuário e armazena na variável enrollments.
    context = {
        'enrollments': enrollments
    }
    return context

# @register.assignment_tag (OBSOLETO)
# Tag simples. Não é obrigatório passar um template como parâmetro, o que permite personalizar o html que será renderizado quando 
# a tag for chamada.
@register.simple_tag 
def load_my_courses(user):
    return Enrollment.objects.filter(user=user) # Retorna todas as inscrições do usuário.