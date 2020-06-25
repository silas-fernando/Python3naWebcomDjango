from django.db import models
from django.urls import reverse
from django.conf import settings

from simplemooc.core.mail import send_mail_template

class CourseManager(models.Manager):

	def search(self, query):
		return self.get_queryset().filter(
			models.Q(name__icontains=query) | models.Q(description__icontains=query)
	)

class Course(models.Model):

	name = models.CharField('Nome', max_length=100)
	slug = models.SlugField('Atalho')
	description = models.TextField('Descrição Simples', blank=True)
	about = models.TextField('Sobre o Curso', blank=True)
	start_date = models.DateField(
		'Data de Início', null=True, blank=True
	)
	image = models.ImageField(
		upload_to='courses/images', verbose_name='Imagem',
		null=True, blank=True
	)

	created_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)

	objects = CourseManager()

	def __str__(self):
		return self.name

	""" OBSOLETE
	@model.permalink
	def get_absolute_url(self):
		return ('courses:details', (), {'slug': self.slug})
	"""
	def get_absolute_url(self):
		return reverse('courses:details', args=(self.slug,))

	class Meta:
		verbose_name = 'Curso'
		verbose_name_plural = 'Cursos'
		ordering = ['name']

class Enrollment(models.Model): # Model inscrição

	# Situações possíveis que o inscrição pode assumir.
	STATUS_CHOICES = (
		(0, 'Pendente'),
		(1, 'Aprovado'),
		(2, 'Cancelado'),
	)

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL, verbose_name='Usuário',
		on_delete=models.PROTECT, related_name='enrollments'
	)
	course = models.ForeignKey(
		Course, verbose_name='Curso', on_delete=models.PROTECT, 
		related_name='enrollments'
	)
	status = models.IntegerField( # Serve para verificar a situação do curso, se o aluno realmente foi inscrito.
		'Situação', choices=STATUS_CHOICES, default=0, blank=True
	)

	created_at = models.DateTimeField('Criado em', auto_now_add=True) # Serve para registrar a data de criação de cada inscrição
	updated_at = models.DateTimeField('Atualizado em', auto_now=True) # Serve para registrar a data das aterações feitas nas incrições.

	def active(self): # Aprova a inscrição do aluno no curso.
		self.status = 1
		self.save()

	def is_approved(self):
		return self.status == 1
		
	class Meta:
		verbose_name = 'Inscrição'
		verbose_name_plural = 'Inscrições'
		unique_together = (('user', 'course'),) # Índice de unicidade. Serve para evitar que o aluno se cadastre duas vezes no mesmo curso

class Announcement(models.Model):

	course = models.ForeignKey(
		Course, verbose_name='Curso', on_delete=models.PROTECT,
		related_name='announcements'
	)
	title = models.CharField('Título', max_length=100)
	content = models.TextField('Conteudo')

	created_at = models.DateTimeField('Criado em', auto_now_add=True) # Serve para registrar a data de criação de cada anúncio.
	updated_at = models.DateTimeField('Atualizado em', auto_now=True) # Serve para registrar a data das aterações feitas nos anúncios.

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Anúncio'
		verbose_name_plural = 'Anúncios'
		ordering = ['-created_at']

class Comment(models.Model):

	announcement = models.ForeignKey(
		Announcement, verbose_name='Anúncio',
		on_delete=models.PROTECT, related_name='comments'
	)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='usuário', on_delete=models.PROTECT)
	comment = models.TextField('Comentário')

	created_at = models.DateTimeField('Criado em', auto_now_add=True) # Serve para registrar a data de criação de cada comentário.
	updated_at = models.DateTimeField('Atualizado em', auto_now=True) # Serve para registrar a data das aterações feitas nos comentários.

	class Meta:
		verbose_name = 'Comentário'
		verbose_name_plural = 'Comentários'
		ordering = ['created_at']

def post_save_announcement(instance, created, **kwargs): # Gatilho que dispara um email depois de salvar um anúncio para todos os usuários do curso em questão.
	if created:
		subject = instance.title
		context = {
			'announcement': instance
		}
		template_name = 'courses/announcement_mail.html'
		enrollments = Enrollment.objects.filter(
			course=instance.course, status=1
		)
		for enrollment in enrollments:
			recipient_list = [enrollment.user.email]
			send_mail_template(subject, template_name, context, recipient_list)

# Cadastra o sinal/gatilho passando o sinal em si, o model que ele vai ficar vinculado 
# e o dispatch_uid, para evitar que mais de um sinal seja gravado para uma mesma função.
models.signals.post_save.connect( 
	post_save_announcement, sender=Announcement, dispatch_uid='post_save_announcement'
)
