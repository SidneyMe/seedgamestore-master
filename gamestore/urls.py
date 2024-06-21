from django.urls import path, include
from .views import IndexView, RegistrationView, ProfileView, GameView, GameCreateView, TagCreateView, GameUpdateView, CustomLoginView, delete_game, payment_view, switch_to_developer, confirm_email

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('signup', RegistrationView.as_view(), name="signup"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('activate/<str:key>', confirm_email, name="confirm_email"),
    path('profile/<int:pk>', ProfileView.as_view(), name="profile"),
    path('profile/switch-to-developer', switch_to_developer, name="switch_to_developer"),
    path('game/<int:pk>', GameView.as_view(), name="game"),
    path('game/add', GameCreateView.as_view(), name="game_create"),
    path('game/update/<int:pk>', GameUpdateView.as_view(), name="game_update"),
    path('game/delete/<int:pk>', delete_game, name="game_delete"),
    path('tag/add', TagCreateView.as_view(), name="add_tag"),
    path('charge/', payment_view, name="charge"),
    path('payment', payment_view, name="payment_success"),
]
