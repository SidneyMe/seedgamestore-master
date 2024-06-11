from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from hashlib import md5
from .forms import CustomUserCreationForm, CreateGameForm, SearchForm, CreateTagForm, CustomAuthenticationForm
from .models import User, Game, Payment
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from simple_email_confirmation.models import EmailAddress
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView


SQLITESAFE = False


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm   


class IndexView(generic.ListView):
    
    model = Game
    template_name = "index.html"
    paginate_by = 12


    def get_queryset(self):

        qs = Game.objects.all()

        try:
            max_price = int(self.request.GET.get("maxprice"))
        except:
            max_price = -1
        if max_price >= 0:
            qs = qs.filter(price__lte=max_price)

        keywords = self.request.GET.get("keywords", "").split(" ")
        for word in keywords:
            qs = qs.filter(name__icontains=word)

        tags = self.request.GET.get("tags", "")
        if len(tags) > 2:
            try:
                tags_id = list(map(int, tags[1:-1].split("|")))
                qs = qs.filter(tags__in=tags_id)
            except:
                pass

        qs = qs.distinct()
        sortby = self.request.GET.get("sortby", "recent")
        if sortby == "recent":
            qs = qs.order_by("-created", "name")
        elif sortby == "cheapest":
            qs = qs.order_by("price", "name")
        else:
            qs = qs.order_by("name")

        return qs


    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        objects = context["object_list"]
        for game in objects:
            if not self.request.user.is_authenticated:
                game.possessed = False
            else:
                game.possessed = Payment.objects.filter(user=self.request.user).filter(game=game).exists()

            game.gtags = list(game.tags.all())

            if SQLITESAFE:
                game.checksum = 0
                continue
            next_payment_id = "{}-{}".format(game.id, get_next_id(Payment))
            game.next_payment_id = next_payment_id
        context["object_list"] = objects

        form = SearchForm(self.request.GET)
        context["form"] = form

        if context["is_paginated"]:
            page_range = list(context["paginator"].page_range)
            page_number = context["page_obj"].number
            if len(page_range) <= 3:
                context["custom_range"] = page_range
            elif page_number == 1:
                context["custom_range"] = page_range[:3]
            elif context["page_obj"].number == context["paginator"].num_pages:
                context["custom_range"] = page_range[-3:]
            else:
                context["custom_range"] = page_range[page_number-2:page_number+1]
        return context


class GameView(generic.DetailView):

    model = Game
    template_name = "game.html"

    def get(self, request, *args, pk=None, **kwargs):

        if not request.user.is_authenticated:
            possessed = False
        else:
            possessed = Payment.objects.filter(user=request.user).filter(game__id=pk).exists()

        if possessed:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseNotFound("Ця гра не існує або ви не є її власником.")


class GameCreateView(generic.FormView):

    form_class = CreateGameForm
    template_name = "game_create.html"
    success_url = "/"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        elif not request.user.is_developer:
            return HttpResponseRedirect(reverse("profile", request.user.id))
        else:
            return super().get(request, *args, **kwargs)

    def get_initial(self):
        return {"developer": self.request.user.id}

    def form_valid(self, form):
        if (not self.request.user.is_developer) or form.cleaned_data["developer"] != self.request.user:
            return HttpResponse('Несанкціоновано', status=401)
        if form.cleaned_data["price"] > 1000:
            form.add_error('price', 'Ціна гри не може перевищувати 1000 доларів США.')
            return self.form_invalid(form)
        game = form.save()
        Payment.objects.get_or_create(user=self.request.user, game=game, amount=0)
        return HttpResponseRedirect(self.get_success_url())


class GameUpdateView(generic.UpdateView):

    model = Game
    form_class = CreateGameForm
    template_name = "game_update.html"
    success_url = "/"

    def get(self, request, *args, pk=None, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        elif Game.objects.get(id=pk).developer != request.user:
            return HttpResponse('Несанкціоновано', status=401)
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["game"] = self.get_object()
        return context

    def get_initial(self):
        return {"developer": self.request.user.id}

    def form_valid(self, form):
        if self.request.user != self.get_object().developer:
            return HttpResponse('Несанкціоновано', status=401)
        form.save()
        return super().form_valid(form)


@login_required
def delete_game(request, pk):
    game = Game.objects.get(id=pk)
    if request.user == game.developer:
        game.delete()
    return HttpResponseRedirect("/")


def payment_view(request):
    msg = "Ваш платіж був УСПІШНИМ!!"
    if request.method == 'POST':
        game_id = request.POST.get("pid").split("-")[0]
        game = Game.objects.get(id=game_id)
        Payment.objects.create(user=request.user, game=game, amount=game.price)
        msg = "Ваш платіж був УСПІШНИМ!"
        return redirect('payment_success')
    elif request.GET.get("result", "error") == "success":
        if "success" in request.path:
            game_id = request.GET["pid"].split("-")[0]
            game = Game.objects.get(id=game_id)
            Payment.objects.create(user=request.user, game=game, amount=game.price)
            msg = "Ваш платіж був УСПІШНИМ!"
    elif "cancel" in request.path:
        msg = "Ваш платіж був СКАСОВАНИМ!"
    elif "error" in request.path:
        msg = "Ваш платіж мав ПОМИЛКУ!"
    return render(request, "payment.html", {"msg": msg})



def get_next_id(model_class):
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(id) FROM {}".format(model_class._meta.db_table))
    row = cursor.fetchone()
    cursor.close()
    return (row[0] if row[0] else 0) + 1


class TagCreateView(generic.FormView):
    form_class = CreateTagForm
    template_name = "tag_create.html"
    success_url = "/tag/add"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        else:
            return super().get(request, *args, **kwargs)
 
    def form_valid(self, form):
        print("Form is valid")
        print("Form data:", form.cleaned_data)
        tag = form.save()
        print("Saved tag:", tag)
        return HttpResponse("tag created")
    
    def form_invalid(self, form):
        print("Form is not valid")
        print("Form errors:", form.errors)
        return super().form_invalid(form)


class RegistrationView(generic.FormView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = "/"
    
    def form_valid(self, form):
        form.save()
        user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
        login(self.request, user)
        link = reverse("confirm_email", kwargs={"key": user.confirmation_key})
        send_mail(
            "Підтвердження електронної пошти для Seed Store", 
            "Ласкаво просимо на наш веб-сайт!", 
            from_email="seedgamestore1@outlook.com",
            recipient_list=[user.email], 
            html_message='<p>Використовуйте це посилання для підтвердження вашої електронної пошти: <a href="http://{}{}">http://{}{}</a></p>'.format(
                self.request.META['HTTP_HOST'], 
                link, 
                self.request.META['HTTP_HOST'], 
                link
            )
        )
        if form.cleaned_data["is_developer"]:
            user.is_developer = True
            user.save()
        return super().form_valid(form)


def confirm_email(request, key):
    email = EmailAddress.objects.get(key=key)
    email.user.confirm_email(key)
    messages.add_message(request, messages.INFO, "Електронна пошта підтверджена!")
    return HttpResponseRedirect("/")


class ProfileView(generic.DetailView):
    
    model = User
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payments = Payment.objects.filter(user=self.request.user)
        context["payments"] = payments
        context["total_spent"] = sum(payment.amount for payment in payments)
        my_games = Game.objects.filter(developer=self.request.user)
        for game in my_games:
            game.sales = Payment.objects.filter(game=game).filter(user=self.request.user).count()
        context["my_games"] = my_games
        if self.request.user.is_developer:
            context["developer"] = self.request.user
            context["token"] = self.request.user.get_token()
        else:
            context["developer"] = False
        return context


@login_required
def switch_to_developer(request):
    
    request.user.is_developer = True
    request.user.save()
    return HttpResponseRedirect(reverse("profile", kwargs={"pk": request.user.id}))
