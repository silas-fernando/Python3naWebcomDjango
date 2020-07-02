from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.conf import settings

from model_mommy import mommy

from simplemooc.courses.models import Course

class CourseManagerTestCase(TestCase):

    def setUp(self): # Função executada para cada teste antes de sua inicialização.
        self.courses = mommy.make(
            'courses.Course', name='Python na Web com Django', _quantity=5
        ) # Retorna uma lista com 10 cursos contendo valores aleatórios, menos para os campos que foram passados como parâmetro.
        self.courses = mommy.make(
            'courses.Course', name='Python para Devs', _quantity=10
        ) # Retorna uma lista com 10 cursos contendo valores aleatórios, menos para os campos que foram passados como parâmetro.
        self.cleint = Client()

    def tearDown(self): # Função executada para cada teste depois da sua finalização.
        Course.objects.all().delete() # Apaga todos os objetos instanciados de Course.

    def test_course_search(self): # Testa se todos os cursos foram criados corretamente.
        search = Course.objects.search('django')
        self.assertEqual(len(search), 5)
        search = Course.objects.search('devs')
        self.assertEqual(len(search), 10)
        search = Course.objects.search('python')
        self.assertEqual(len(search), 15)


