import re

from django.db import models
from django.core import validators
from django.contrib.auth.models import (AbstractBaseUser, # Traz a lógica básica para que o usuário funcione (ex: alterar e criptografar senhas).
                                        PermissionsMixin, # Traz a questão de segurança do Django de permissão e grupos.
                                        UserManager) # Implementa algumas funcões que são importantes para alguns comandos do Django na parte de usuários (ex: criação de superusuário).

class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        'Nome de Usuário', max_length=30, unique=True, 
        validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'), # indica que o username terá um validator conforme a expressão regular.
        'O nome do usuário só pode conter letras, digitos ou os '
        'seguintes caracteres: @/./+/-/_', 'invalid')]
    )
    email = models.EmailField('E-mail', unique=True)
    name = models.CharField('Nome', max_length=100, blank=True)
    is_active = models.BooleanField('Está ativo?', blank=True, default=True) # Serve para saber se o usuário está ativo ou não e se pode logar ou não.
    is_staff = models.BooleanField('É da equipe?', blank=True, default=False) # Serve para saber se o usuário pode acessar a área administrativa.
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True) # Importante para a integração com o Django e para criação de superusuários.
    # auto_now_add=True pega a data atual do salvamento

    objects = UserManager()

    # Os dois campos abaixo é para ser compatível com alguns comandos e algumas outras coisas do Django.
    USERNAME_FIELD = 'username' # Indica qual será o campo único e referência no momento do login.
    REQUIRED_FIELDS = ['email'] # Utilizados no comando de criação de superusuários.

    def __str__(self): # Representação em string do usuário.
        return self.name or self.username # Se o usuário tiver nome, retorna o nome, se não retorna o username.

    def get_short_name(self): # Retorna a descrição curta do nome.
        return self.username

    def get_full_name(self): # Retorna a representação em string do usuário.
        return str(self)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'