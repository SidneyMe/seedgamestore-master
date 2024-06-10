from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from gamestore.models import Payment, Game, Tag
from django.core.validators import MinValueValidator
from ajax_select.fields import AutoCompleteSelectMultipleField


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Ім'я користувача")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Пошта")
    username = forms.CharField(label="Ім'я користувача")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Підтвердіть пароль", widget=forms.PasswordInput)
    is_developer = forms.BooleanField(label="Ви хочете додати свої власні ігри як розробник?", required=False)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email")
        
        
class CreateGameForm(forms.ModelForm):
    name = forms.CharField(label="Назва")
    url = forms.URLField(label="Посилання")
    cover = forms.FileField(label="Обкладинка")
    price = forms.DecimalField(label="Ціна")
    tags = AutoCompleteSelectMultipleField('tags', required=False, help_text="Почніть вводити для пошуку тегів", label="Теги")

    class Meta:
        model = Game
        fields = ["developer", "name", "url", "cover", "price", "tags"]
        widgets = {
            "developer": forms.HiddenInput()
        }


class CreateTagForm(forms.ModelForm):
    name = forms.CharField(label="Назва", max_length=50, required=False)
    
    class Meta:
        model = Tag
        fields = ["name"]


class SearchForm(forms.Form):
    keywords = forms.CharField(label='Ключові слова', max_length=128, required=False, )
    tags = AutoCompleteSelectMultipleField('tags', required=False, help_text="Почніть вводити для пошуку тегів")
    maxprice = forms.IntegerField(label="Максимальна ціна", validators=[MinValueValidator(0)], required=False)
    sortby = forms.ChoiceField(label="Сортувати за", choices=[("recent", "Найновіші"), ("cheapest", "Найдешевша ціна"), ("alpha", "Алфавітний порядок")], required=False)
 

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = []
        widgets = {
            "user": forms.HiddenInput(),
            "game": forms.HiddenInput()
        }
