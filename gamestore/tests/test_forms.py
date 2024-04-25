from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from ajax_select.fields import AutoCompleteSelectMultipleField
from gamestore.forms import PaymentForm, CreateGameForm, CreateTagForm, CustomUserCreationForm, SearchForm
from gamestore.models import Payment, Game, Tag


class CreateGameFormTestCase(TestCase):
    def test_create_game_form_fields(self):
        form = CreateGameForm()
        self.assertEqual(form.Meta.model, Game)
        self.assertEqual(form.Meta.fields, ["developer", "name", "url", "cover", "price", "tags"])
        self.assertEqual(type(form.Meta.widgets), dict)
        self.assertEqual(type(form.Meta.widgets.get('developer')), type(forms.HiddenInput()))
        

class PaymentFormTestCase(TestCase):
    def test_payment_form_fields(self):
        form = PaymentForm()
        self.assertEqual(form.Meta.model, Payment)
        self.assertEqual(form.Meta.exclude, [])
        self.assertEqual(type(form.fields['user'].widget), type(forms.HiddenInput()))
        self.assertEqual(type(form.fields['game'].widget), type(forms.HiddenInput()))

class CreateTagFormTestCase(TestCase):
    def test_create_tag_form_fields(self):
        form = CreateTagForm()
        self.assertEqual(form.Meta.model, Tag)
        self.assertEqual(form.Meta.fields, ["name"])
        

class CustomUserCreationFormTestCase(TestCase):
    def test_custom_user_creation_form_fields(self):
        form = CustomUserCreationForm()
        self.assertEqual(form.Meta.model, get_user_model())
        self.assertEqual(form.Meta.fields, ("username", "email"))
        self.assertEqual(form.fields["email"].label, "Your email address")
        self.assertEqual(form.fields["is_developer"].label, "Do you want to add your own games as a developer?")
        self.assertFalse(form.fields["is_developer"].required)
        


class SearchFormTestCase(TestCase):
    def test_search_form_fields(self):
        form = SearchForm()
        self.assertIsInstance(form.fields['keywords'], forms.CharField)
        self.assertIsInstance(form.fields['tags'], AutoCompleteSelectMultipleField)
        self.assertIsInstance(form.fields['maxprice'], forms.IntegerField)
        self.assertIsInstance(form.fields['sortby'], forms.ChoiceField)

    def test_search_form_clean_tags(self):
        Tag.objects.create(name='valid_tag1')
        Tag.objects.create(name='valid_tag2')

        form = SearchForm()
        form.cleaned_data = {'tags': ['valid_tag1', 'valid_tag2']}
        self.assertEqual(form.clean_tags(), ['valid_tag1', 'valid_tag2'])

    def test_search_form_clean_tags_invalid(self):
        form = SearchForm()
        form.cleaned_data = {'tags': ['tag1', 'tag2', 'invalid_tag']}
        with self.assertRaises(ValidationError):
            form.clean_tags()