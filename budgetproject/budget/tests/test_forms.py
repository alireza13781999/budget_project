from django.test import SimpleTestCase
from budget.forms import ExpenseForm

class TestForms(SimpleTestCase):
    def test_form_valid_data(self):
        form = ExpenseForm(data={
            'title':'ex1',
            'amount':1000,
            'category':'design'
        })

        self.assertTrue(form.is_valid())

    def test_form_no_data(self):
        form = ExpenseForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)