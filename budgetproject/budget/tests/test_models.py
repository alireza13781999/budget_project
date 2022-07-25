from django.test import TestCase
from budget.models import Project, Category, Expense

class TestModels(TestCase):
    def setUp(self):
        self.project1 = Project.objects.create(
            name='project 1',
            budget=6000
        )

    def test_project_assigned_slug(self):
        self.assertEquals(self.project1.slug, 'project-1')

    def test_bdget_left(self):
        category1 = Category.objects.create(
            project=self.project1,
            name='development'
        )
        Expense.objects.create(
            project=self.project1,
            title='ex1',
            amount=1000,
            category=category1
        )

        self.assertEquals(self.project1.budget_left, 5000)

    def test_total_transactions(self):
        project2 = Project.objects.create(
            name='project 2',
            budget=6000
        )

        category = Category.objects.create(
            project=self.project1,
            name='development'
        )

        Expense.objects.create(
            project=self.project1,
            title='ex1',
            amount=1000,
            category=category
        )

        self.assertEquals(self.project1.total_transactions, 1)