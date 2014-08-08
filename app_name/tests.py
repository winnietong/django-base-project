from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.test import TestCase
from test_utils import run_pyflakes_for_package, run_pep8_for_package

# Create your tests here.

class SyntaxTest(TestCase):
    def test_syntax(self):
        """
        Run pyflakes/pep8 across the code base to check for potential errors.
        """
        packages = ['teach_app']
        warnings = []
        # Eventually should use flake8 instead so we can ignore specific lines via a comment
        for package in packages:
            warnings.extend(run_pyflakes_for_package(package, extra_ignore=("_settings",)))
            warnings.extend(run_pep8_for_package(package, extra_ignore=("_settings",)))
        if warnings:
            self.fail("{0} Syntax warnings!\n\n{1}".format(len(warnings), "\n".join(warnings)))


class ViewTest(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertIn('Class Tracker', response.content)

    def test_dashboard_page(self):
        response = self.client.get(reverse('dashboard'))
        self.assertIn('Latest', response.content)

    def test_exercise_page(self):
        response = self.client.get(reverse('exercises'))
        self.assertIn('Exercises', response.content)

    def test_students_page(self):
        response = self.client.get(reverse('students'))
        self.assertIn('Students', response.content)


class FormTest(TestCase):
    def test_login(self):
        User.objects.create_user(username='test_user', email='test@gmail.com', password='123')

        data = {
            'username': 'test_user',
            'password': '123'
        }

        response = self.client.post(reverse('login'), data)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertTrue(response.get('location').endswith(reverse('dashboard')))

    def test_exercise(self):
        data = {
            'name': 'Ex 2',
            'description': 'testing',
            'due_date': '2014-10-20',
            'difficulty': 'Easy'
        }
        response = self.client.post(reverse('add_exercise'), data)
        self.assertTrue(Exercise.objects.filter(name='Ex 2'))
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertTrue(response.get('location').endswith(reverse('exercises')))

    def test_register(self):
        data = {
            'username': 'john14',
            'email': 'john@gmail.com',
            'password1': '123',
            'password2': '123',
            'type': 'Student'
        }
        response = self.client.post(reverse('register'), data)
        self.assertTrue(User.objects.filter(username='john14'))
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertTrue(response.get('location').endswith(reverse('home')))
