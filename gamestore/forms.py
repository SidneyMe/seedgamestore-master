from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from gamestore.models import Payment, Game, Tag
from django.core.validators import MinValueValidator
from django_select2.forms import Select2MultipleWidget

class SearchForm(forms.Form):
    keywords = forms.CharField(
        label='Ключові слова', 
        max_length=128, 
        required=False,
        widget=forms.TextInput(attrs={'id': 'id_keywords'})
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=Select2MultipleWidget(attrs={'id': 'id_tags'}),
        required=False,
        help_text="Почніть вводити для пошуку тегів"
    )
    maxprice = forms.IntegerField(
        label="Максимальна ціна", 
        validators=[MinValueValidator(0)], 
        required=False,
        widget=forms.NumberInput(attrs={'id': 'id_maxprice'})
    )
    sortby = forms.ChoiceField(
        label="Сортувати за", 
        choices=[
            ("recent", "Найновіші"), 
            ("cheapest", "Найдешевша ціна"), 
            ("alpha", "Алфавітний порядок")
        ], 
        required=False,
        widget=forms.Select(attrs={'id': 'id_sortby'})
    )

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
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=Select2MultipleWidget,
        required=False,
        help_text="Почніть вводити для пошуку тегів"
    )

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
 

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = []
        widgets = {
            "user": forms.HiddenInput(),
            "game": forms.HiddenInput()
        }
