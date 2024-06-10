from django.http import JsonResponse, HttpResponseForbidden
from django.core import serializers
from gamestore.models import Game, User
from simple_email_confirmation.models import EmailAddress

def check_token(token):
    try:
        email = EmailAddress.objects.get(key=token)
        return email.user
    except EmailAddress.DoesNotExist:
        return False


def get_games(request):
    if request.method == "GET":
        try:
            token = request.GET["token"]
            user = check_token(token)
            if not user:
                raise KeyError
            games = Game.objects.all()
            data = serializers.serialize("json", games)
            return JsonResponse(data, safe=False)
        except KeyError:
            return HttpResponseForbidden("Token not accepted.")


def get_my_games(request):
    if request.method == "GET":
        try:
            token = request.GET["token"]
            user: User = check_token(token)
            if not user:
                raise KeyError
            elif not user.is_developer:
                raise PermissionError
            games = Game.objects.filter(developer=user)
            data = serializers.serialize("json", games)
            return JsonResponse(data, safe=False)
        except KeyError:
            return HttpResponseForbidden("Token not accepted.")
        except PermissionError:
            return HttpResponseForbidden("Your account is not a developer account.")