from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):

    email = forms.EmailField(label='E-mail')

    # Verifica se o email digitado já pertence a algum usuário.
    def clean_email(self):
        email = self.cleaned_data['email'] # Recupera o email digitado.
        if User.objects.filter(email=email).exists(): # Verifica se o email recuperado já existe no banco de dados.
            raise forms.ValidationError('Já existe um usuário com este e-mail') # raise = Lança uma exeção com a mensagem informada.
        return email # Se nã existe retorna o email recuperado.
    # Fim verifica se o email digitado já pertence a algum usuário.

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# ModelForm = formulário específico para um modelo.
# Pega todos os campos do modelo e gera um formulário
# baseado nesses campos já predefinidos.

class EditAccountForm(forms.ModelForm):

    # Verifica se o email digitado já pertence a algum usuário.
    def clean_email(self):
        email = self.cleaned_data['email'] # Recupera o email digitado.
        queryset = User.objects.filter(email=email).exclude(pk=self.instance.pk) # instance = armazena o email do usuário em questão. 
        # O queryset recebe todos os emails do banco de dados, exceto o email do usuário que está sendo editado no momento.
        if queryset.exists(): # Se houver alteração no email, verifica se o novo email já existe no banco de dados.
            raise forms.ValidationError('Já existe um usuário com este e-mail') # raise = Lança uma exeção com a mensagem informada.
        return email # Se nã existe retorna o email recuperado.
    # Fim verifica se o email digitado já pertence a algum usuário.

    class Meta:
        model = User # Informa qual Model será usado para gerar o Form.
        fields = ['username', 'email', 'first_name', 'last_name'] # Esses são os campos já predefinidos do Model User do Django que serão usados. 
    