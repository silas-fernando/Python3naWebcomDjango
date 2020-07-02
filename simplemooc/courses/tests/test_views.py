from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.conf import settings

from simplemooc.courses.models import Course

class ContactCourseTestCase(TestCase):

    def setUp(self): # Função executada para cada teste antes de sua inicialização.
        self.course = Course.objects.create(name='Django', slug='django')
    
    def tearDown(self): # Função executada para cada teste depois da sua finalização.
        self.course.delete()

    """
    @classmethod
    def setUpClass(cls): # Função executada para todos os testes antes deles iniciarem.
        pass

    @classmethod
    def tearDownClass(cls): # Função executada depois que todos os testes terminam.
        pass
    """

    def test_contact_form_error(self): # Testa se as mensagens de erro estão sendo exibidas corretamente.
        data = {'name': 'Fulano de Tal', 'email': '', 'message': ''}
        client = Client()
        path = reverse('courses:details', args=[self.course.slug])
        response = client.post(path, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'message', 'Este campo é obrigatório.')

    def test_contact_form_success(self): # Testa se a estrutura do email esta correta.
        data = {'name': 'Fulano de Tal', 'email': 'silasf_primiani@gmail.com', 'message': 'Oi'}
        client = Client()
        path = reverse('courses:details', args=[self.course.slug])
        response = client.post(path, data)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL])


