from django.http import response
from django.test import TestCase, Client, client
from django.urls import reverse
from django.urls.base import resolve
from budget.models import Project, Category, Expense
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.list_url = reverse('list')
        self.detail_url = reverse('detail', args=['test1'])
        self.test1 = Project.objects.create(
            name='test1',
            budget=4000
        )

    def test_project_list_get(self):
        response = self.client.get(self.list_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-list.html')

    def test_project_detail_get(self):
        response = self.client.get(self.detail_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-detail.html')

    def test_project_detail_post_adds_new_expense(self):
        Category.objects.create(
            project=self.test1,
            name='development',
            
        )

        response = self.client.post(self.detail_url, {
            'title': 'expense1',
            'amount': 1000,
            'category': 'development'
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.test1.expenses.first().title, 'expense1')

    def test_project_detail_post_no_data(self):
        response = self.client.post(self.detail_url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.test1.expenses.count(), 0)

    def test_project_detail_delete_expense(self):
        category1 = Category.objects.create(
            project=self.test1,
            name='development',
            
        )

        Expense.objects.create(
            project=self.test1,
            title='expense1',
            amount=1000, 
            category=category1
        )

        response = self.client.delete(self.detail_url, json.dumps({
            'id': 1
        }))

        self.assertEquals(response.status_code, 204)
        self.assertEquals(self.test1.expenses.count(), 0)

    def test_project_detail_delete_no_id(self):
        category1 = Category.objects.create(
            project=self.test1,
            name='development',
            
        )

        Expense.objects.create(
            project=self.test1,
            title='expense1',
            amount=1000, 
            category=category1
        )

        response = self.client.delete(self.detail_url)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(self.test1.expenses.count(), 1)
    
    def test_project_create_post(self):
        url = reverse('add')
        response = self.client.post(url, {
            'name': 'test2',
            'budget': 10000,
            'categoriesString': 'design,development'
        })

        test2 = Project.objects.get(id=2)
        self.assertEquals(test2.name, 'test2')

        first_category = Category.objects.get(id=1)
        self.assertEquals(first_category.project, test2)
        self.assertEquals(first_category.name, 'design')

        second_category = Category.objects.get(id=2)
        self.assertEquals(second_category.project, test2)
        self.assertEquals(second_category.name, 'development')