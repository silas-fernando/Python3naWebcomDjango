from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.conf import settings

from .forms import RegisterForm

def register(request):
    template_name = 'accounts/register.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Autenticação do usuário
            user = form.save()
            user = authenticate(
                username=user.username, password=form.cleaned_data['password1']
            )
            # Fim da autenticação do usuário
            login(request, user) # Basicamente coloca o usuário na sessão
            return redirect('core:home') # Redireciona o usuário para a página home
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)
