from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Course, Enrollment
from .forms import ContactCourse

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
def enrollment(request, slug):
	course = get_object_or_404(Course, slug=slug) # Recupera o curso atual.
	enrollment, created = Enrollment.objects.get_or_create(
		user=request.user, course=course
	) # Pega, ou se não houver, cria uma inscrição para o usuário atual em um determinado curso.
	# if created: # Se uma nova inscrição foi criado, ela já é ativada.
		# enrollment.active() 
	return redirect('accounts:dashboard')