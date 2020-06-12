from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class PasswordResetForm(forms.Form):

    email = forms.EmailField(label='E-mail')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists(): # Verifica se existe algum usuário com o email informado pelo usuário.
            return email # Se sim, retorna o email.
        raise forms.ValidationError(
            'Nenhum usuário encontrado com este e-mail' # Se não, lança uma exceção e apresenta esta mensagem ao usuário.
        )

class RegisterForm(forms.ModelForm):

    # email = forms.EmailField(label='E-mail')
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)


    """ Verifica se o email digitado já pertence a algum usuário.
    def clean_email(self):
        email = self.cleaned_data['email'] # Recupera o email digitado.
        if User.objects.filter(email=email).exists(): # Verifica se o email recuperado já existe no banco de dados.
            raise forms.ValidationError('Já existe um usuário com este e-mail') # raise = Lança uma exeção com a mensagem informada.
        return email # Se nã existe retorna o email recuperado.
    """

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1") # Recupera a senha digitada pelo usuário.
        password2 = self.cleaned_data.get("password2") # Recupera a confirmação de senha digitada pelo usuário.
        if password1 and password2 and password2 != password2: # Verifica se os dois campos estão preenchidos e se seus conteudos são diferentes.
            raise forms.ValidationError('A confirmação de senha não está correta.') # Se não foram preenchidos ou se forem iguais apresenta esta mensagem de erro.
        return password2 

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False) # Chama o super do RegisterForm e o save com um commit falso para não salvar, para receber o usuário.
        user.set_password(self.cleaned_data['password1']) # Seta e criptografa a senha
        # user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
    class Meta:
        model = User
        fields = ['username', 'email']

# ModelForm = formulário específico para um modelo.
# Pega todos os campos do modelo e gera um formulário
# baseado nesses campos já predefinidos.

class EditAccountForm(forms.ModelForm):

    """ Verifica se o email digitado já pertence a algum usuário.
    def clean_email(self):
        email = self.cleaned_data['email'] # Recupera o email digitado.
        queryset = User.objects.filter(email=email).exclude(pk=self.instance.pk) # instance = armazena o email do usuário em questão. 
        # O queryset recebe todos os emails do banco de dados, exceto o email do usuário que está sendo editado no momento.
        if queryset.exists(): # Se houver alteração no email, verifica se o novo email já existe no banco de dados.
            raise forms.ValidationError('Já existe um usuário com este e-mail') # raise = Lança uma exeção com a mensagem informada.
        return email # Se nã existe retorna o email recuperado.
    """ 

    class Meta:
        model = User # Informa qual Model será usado para gerar o Form.
        fields = ['username', 'email', 'name'] # Esses são os campos do Model User do Django que serão usados. 
    