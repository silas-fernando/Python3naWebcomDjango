from django.db import models
from django.urls import reverse
from django.conf import settings

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