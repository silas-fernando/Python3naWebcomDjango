from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages

from simplemooc.core.utils import generate_hash_key
from simplemooc.courses.models import Enrollment

from .forms import RegisterForm, EditAccountForm, PasswordResetForm
from .models import PasswordReset

User = get_user_model()

# @login_required verifica se o usuário está logado antes de executar a função logo abaixo dele.
# Se sim, redireciona para o painel do usuário. Senão, redireciona para a página de login.
@login_required
def dashboard(request):
    template_name = 'accounts/dashboard.html'
    context = {}
    context['enrollments'] = Enrollment.objects.filter(user=request.user) # Permite que os cursos sejam carregados dinâmicamente no dashboard do usuário.
    return render(request, template_name, context)

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

def password_reset(request):
    template_name = 'accounts/password_reset.html'
    context = {}
    form = PasswordResetForm(request.POST or None) # Envia o form se houver dados nele ou se estiver vazio.
    if form.is_valid(): # Só valida se houver dados no form ou se ele estiver vazio.
        form.save()
        context['success'] = True # Variável do template usada para informar ao usuário se os dados foram ou não validados recebe True.
    context['form'] =  form
    return render(request, template_name, context)

def password_reset_confirm(request, key):
    template_name = 'accounts/password_reset_confirm.html'
    context = {}
    reset = get_object_or_404(PasswordReset, key=key) # Pega a chave que está no html e busca o model.
    form = SetPasswordForm(user=reset.user, data=request.POST or None) # Se não der o erro 404 acima, faz o reset.user
    if form.is_valid():
        form.save()
        context['success'] = True # Variável do template usada para informar ao usuário se os dados foram ou não validados recebe True.
    context['form'] = form # Adiciona o form ao contexto
    return render(request, template_name, context)

# @login_required verifica se o usuário está logado antes de executar a função logo abaixo dele.
# Se sim, redireciona para o painel do usuário. Senão, redireciona para a página de login.
@login_required
def edit(request):
    template_name = 'accounts/edit.html'
    context = {}
    if request.method == 'POST': # Verifica se o método de transferência de dados do form é POST
        form = EditAccountForm(request.POST, instance=request.user) # Se for POST, form recebe os dados e o usuário atual da sessão
        if form.is_valid(): # Se o formulário estiver válido
            form.save() # Salva os dados do form no bd
            messages.success(request, 'Os dados da sua conta foram alterados com sucesso')
            # form = EditAccountForm(instance=request.user) # Limpa os campos do form
            # context['success'] = True # Variável do template usada para mostrar ao usuário que os dados foram alterados com sucesso
            return redirect('accounts:dashboard')
    else: # Se não for POST
        form = EditAccountForm(instance=request.user) # Apenas limpa os campos do formulário
    context['form'] = form # Variável form do tamplate recebe o form atualizado
    return render(request, template_name, context) # Renderiza o novo template com as novas alterações

@login_required
def edit_password(request):
    template_name = 'accounts/edit_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user) # Como é um form um pouco diferente, os parâmetros vão nomeados para não ter erro.
        if form.is_valid():
            form.save()
            context['success'] = True
    else:
        form = PasswordChangeForm(user=request.user) 
    context['form'] = form
    return render(request, template_name, context)