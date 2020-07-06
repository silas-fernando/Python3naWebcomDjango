from django.db import models
from django.conf import settings

from taggit.managers import TaggableManager


class Thread(models.Model):

    title = models.CharField('Titulo', max_length=100)
    body = models.TextField('Mensagem')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Autor',
        on_delete=models.PROTECT, related_name='threads'
    )  # related_name='threads' é uma referência no autor para todos os tópicos que ele criou.

    # Contabiliza as visualizações.
    views = models.IntegerField('Visualizações', blank=True, default=0)
    answers = models.IntegerField('Respostas', blank=True, default=0)

    tags = TaggableManager()

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:  # Serve para melhorar a página admin.
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-modified']


class Reply(models.Model):

    reply = models.TextField('Resposta')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Autor',
        on_delete=models.PROTECT, related_name='replies'
    )  # related_name='threads' é uma referência no autor para todos os tópicos que ele criou.
    # correct Serve para o usuário indicar qual é a resposta correta para a sua dúvida.
    correct = models.BooleanField('Correta?', blank=True, default=False)

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    def __str__(self):
        return self.reply[:100]  # Retorna as primeiras 100 letras da resposta.

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        # ordering :rioritariamente ordena pela resposta correta indicada pelo usuário.
        ordering = ['-correct', 'created']
