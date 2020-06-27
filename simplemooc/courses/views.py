from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Enrollment, Lesson
from .forms import ContactCourse, CommentForm
from .decorators import enrollment_required

def index(request):
	courses = Course.objects.all()
	template_name = 'courses/index.html'
	context = {
		'courses': courses
	}
	return render(request, template_name, context)

"""
def details(request, pk):
	course = get_object_or_404(Course, pk=pk)
	context = {
		'course': course
	}
	template_name = 'courses/details.html'
	return render(request, template_name, context)
"""
def details(request, slug):
	course = get_object_or_404(Course, slug=slug)
	context = {}
	if request.method == 'POST':
		form = ContactCourse(request.POST)
		if form.is_valid():
			context['is_valid'] = True
			form.send_mail(course)
			print(form.cleaned_data)
			form = ContactCourse()
	else:
		form = ContactCourse()
	context['form'] = form
	context['course'] = course
	template_name = 'courses/details.html'
	return render(request, template_name, context)

@login_required # Obriga o usuário estar logado.
def enrollment(request, slug): # View Inscrição.
	course = get_object_or_404(Course, slug=slug) # Recupera o curso atual.
	enrollment, created = Enrollment.objects.get_or_create(
		user=request.user, course=course
	) # Pega, ou se não houver, cria uma inscrição para o usuário atual em um determinado curso.
	if created: 
		enrollment.active() 
		messages.success(request, 'Inscrição efetuada com sucesso')
	else:
		messages.info(request, 'Você já esta inscrito nesse curso')
	
	return redirect('accounts:dashboard')

@login_required
def undo_enrollment(request, slug): # View para cancelar inscrição.
	course = get_object_or_404(Course, slug=slug) # Recupera o curso atual.
	enrollment = get_object_or_404( # Verifica se ele está inscrito no curso.
		Enrollment, user=request.user, course=course
	)
	if request.method == 'POST':
		enrollment.delete()
		messages.success(request, 'Sua inscrição foi cancelada com sucesso')
		return redirect('accounts:dashboard')
	template = 'courses/undo_enrollment.html'
	context = {
		'enrollment': enrollment,
		'course': course,
	}
	return render(request, template, context)

@login_required # Obriga o usuário estar logado.
@enrollment_required # Verifica se o usuário está inscrito e aprovado para acessar determinado curso.
def announcements(request, slug): # View anúncios.
	course = request.course # recupera o curso do request que será passado pelo decorator @enrollment_required.
	template = 'courses/announcements.html'
	context = {
		'course': course,
		'announcements': course.announcements.all()
	}
	return render(request, template, context)

@login_required # Obriga o usuário estar logado.
@enrollment_required # Verifica se o usuário está inscrito e aprovado para acessar determinado curso.
def show_announcement(request, slug, pk): # View para exibir os anúncios.
	course = request.course # recupera o curso do request que será passado pelo decorator @enrollment_required.
	announcement = get_object_or_404(course.announcements.all(), pk=pk)
	form = CommentForm(request.POST or None)
	if form.is_valid():
		comment = form.save(commit=False) # Cria o objeto, atribui os valores preenchidos ao objeto, mas não salva de fato.
		comment.user = request.user # Informa qual é o usuário.
		comment.announcement = announcement # Informa qual é o anúncio.
		comment.save() # Agora cria o objeto, atribui os valores preenchidos e salva.
		form = CommentForm() # Limpa o form do comentário.
		messages.success(request, 'Seu comentário foi enviado com sucesso')
	template = 'courses/show_announcements.html'
	context = {
		'course': course, 
		'announcement': announcement,
		'form': form,
	}
	return render(request, template, context)

@login_required
@enrollment_required
def lessons(request, slug):
	course = request.course # recupera o curso do request que será passado pelo decorator @enrollment_required.
	template = 'courses/lessons.html'
	lessons = course.release_lessons()
	if request.user.is_staff:
		lessons = course.lessons.all()
	context = {
		'course': course,
		'lessons': lessons
	}
	return render(request, template, context)

@login_required
@enrollment_required
def lesson(request, slug, pk):
	course = request.course # recupera o curso do request que será passado pelo decorator @enrollment_required.
	lesson = get_object_or_404(Lesson, pk=pk, course=course)
	if not request.user.is_staff and not lesson.is_available():
		messages.error(request, 'Esta aula não esta disponível')
		return redirect('courses:lessons', slug=course.slug)
	template = 'courses/lesson.html'
	context = {
		'course': course,
		'lesson': lesson
	}
	return render(request, template, context)
