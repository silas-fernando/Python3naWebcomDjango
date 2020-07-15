from django.db import models
from django.conf import settings
from django.urls import reverse

from taggit.managers import TaggableManager


class Thread(models.Model):

    title = models.CharField('Titulo', max_length=100)
    slug = models.SlugField('Identificador', max_length=100, unique=True)
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

    """ OBSOLETO
	@model.permalink
	def get_absolute_url(self):
        return('forum:thread', (), {'slug': self.slug})
	"""

    # def get_absolute_url(self):
    #    return reverse('forum:thread', args=(self.slug,))

    def get_absolute_url(self):
        return reverse('forum:thread', args=(self.slug,))

    class Meta:  # Serve para melhorar a página admin.
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-modified']


class Reply(models.Model):

    thread = models.ForeignKey(
        Thread, verbose_name='Tópico',
        on_delete=models.PROTECT, related_name='replies'
    )
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


# Toda vez que uma resposta é criada, essa função é executada em seguida.
def post_save_reply(created, instance, **kwargs):
    instance.thread.answers = instance.thread.replies.count()
    instance.thread.save()
    if instance.correct:  # Verifica se a resposta em questão é a correta.
        # Busca todas as resposta, exceto a correta do tópico em questão.
        instance.thread.replies.exclude(pk=instance.pk).update(
            # Atribui falso para todas as respostas encontradas acima.
            correct=False
        )


# Toda vez que uma resposta é removida, essa função é executada em seguida.
def post_delete_reply(instance, **kwargs):
    instance.thread.answers = instance.thread.replies.count()
    instance.thread.save()


models.signals.post_save.connect(
    post_save_reply, sender=Reply, dispatch_uid='post_save_reply'
)
models.signals.post_delete.connect(
    post_delete_reply, sender=Reply, dispatch_uid='post_delete_reply'
)
