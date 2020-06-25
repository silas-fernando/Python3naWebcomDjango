from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Enrollment
from .forms import ContactCourse, CommentForm

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
	if created: # Se uma nova inscrição foi criado, ela já é ativada.
		# enrollment.active() 
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
def announcements(request, slug): # View anúncios.
	course = get_object_or_404(Course, slug=slug) # Recupera o curso atual.
	if not request.user.is_staff: # Se o usuário não for membro do grupo de administradores.
		enrollment = get_object_or_404( # Verifica se ele está inscrito no curso.
			Enrollment, user=request.user, course=course
		)
		if not enrollment.is_approved(): # Se o usuário não estiver sido aprovado no curso.
			messages.error(request, 'A sua inscrição está pendente')
			return redirect('accounts:dashboard')
	template = 'courses/announcements.html'
	context = {
		'course': course,
		'announcements': course.announcements.all()
	}
	return render(request, template, context)

@login_required # Obriga o usuário estar logado.
def show_announcement(request, slug, pk): # View para exibir os anúncios.
	course = get_object_or_404(Course, slug=slug) # Recupera o curso atual.
	if not request.user.is_staff: # Se o usuário não for membro do grupo de administradores.
		enrollment = get_object_or_404( # Verifica se ele está inscrito no curso.
			Enrollment, user=request.user, course=course
		)
		if not enrollment.is_approved(): # Se o usuário não estiver sido aprovado no curso.
			messages.error(request, 'A sua inscrição está pendente')
			return redirect('accounts:dashboard')
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