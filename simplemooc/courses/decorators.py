from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import Course, Enrollment

def enrollment_required(view_func): # Essa função recebe a view que será executado pelo django.
    def _wrapper(request, *args, **kwargs): # Funcção auxiliar para indicar que isso aqui seria nossa view de fato.
        slug = kwargs['slug'] # Primeiramente busca o slug do curso. Para usar esse decorator, é obrigatório colocar o slug do curso na url.
        course = get_object_or_404(Course, slug=slug) # Pega o curso atual.
        has_permission = request.user.is_staff # Se o usuário for staff ele terá permissão automaticamente.
        if not has_permission: # Se não for staff.
            try:
                enrollment = Enrollment.objects.get(
                    user=request.user, course=course # Busca a matrícula fazendo a relação de usuário e curso.
                )
            except Enrollment.DoesNotExist: # Se não existeir a matrícula para o curso em questão.
                message = 'Desculpe, mas você não tem permissão para acessar esta página'
            else:
                if enrollment.is_approved(): # Se existir, será verificado se a inscrição está aprovada.
                    has_permission = True # Se sim, o usuário passará a ter permissão.
                else: # Se não, é por que a inscrição não foi aprovada.
                    message = 'A sua inscrição no curso ainda está pendente'

        # Se de fato o usuário ainda não tiver permissão, será exibido uma mensagem de 
        # erro e ele será redirecionado para o dashboard.
        if not has_permission: 
            messages.error(request, message)
            return redirect('accounts:dashboard')
        request.course = course # Se passar é porque ele tem permissão. Para não repetir a mesma consulta a este curso 
        # lá na view, o objeto curso será passado no request.
        return view_func(request, *args, **kwargs) # Executa a view de fato, que deve ser executada para url em questão.
    return _wrapper