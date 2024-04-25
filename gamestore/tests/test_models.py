from django.test import TestCase
from gamestore.models import User
from django.test import TestCase
from gamestore.models import User, Tag, Game, GameState, Payment
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth import get_user_model
import datetime
import time

class UserModelTestCase(TestCase):
    def test_user_str_representation(self):
        # Create a test user
        user = User.objects.create_user(username="testuser", password="testpassword")

        # Check that the string representation of the user is the username
        self.assertEqual(str(user), "testuser")

    def test_user_is_developer_default_value(self):
        # Create a test user
        user = User.objects.create_user(username="testuser", password="testpassword")

        # Check that the default value of is_developer is False
        self.assertFalse(user.is_developer)

    def test_user_get_token(self):
        # Create a test user
        user = User.objects.create_user(username="testuser", password="testpassword")

        # Call the get_token method
        token = user.get_token()

        # Check that the token is a string
        self.assertIsInstance(token, str)


class UserModelTestCase(TestCase):
    def test_user_str_representation(self):
        # Create a test user
        user = User.objects.create_user(username="testuser", password="testpassword")

        # Check that the string representation of the user is the username
        self.assertEqual(str(user), "testuser")

    def test_user_is_developer_default_value(self):
        # Create a test user
        user = User.objects.create_user(username="testuser", password="testpassword")

        # Check that the default value of is_developer is False
        self.assertFalse(user.is_developer)

    def test_user_get_token(self):
        # Create a test user
        user = User.objects.create_user(username="testuser", password="testpassword")

        # Call the get_token method
        token = user.get_token()

        # Check that the token is a string
        self.assertIsInstance(token, str)


class TagModelTestCase(TestCase):
    def test_tag_str_representation(self):
        # Create a test tag
        tag = Tag(name="testtag")

        # Check that the string representation of the tag is the name
        self.assertEqual(str(tag), "testtag")


class GameModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_game_str_representation(self):
        # Create a test game
        game = Game.objects.create(
            developer=self.user,
            name="Test Game",
            url="https://example.com",
            price=10
        )

        # Check that the string representation of the game is the name
        self.assertEqual(str(game), "Test Game")

    def test_game_get_absolute_url(self):
        # Create a test game
        game = Game.objects.create(
            developer=self.user,
            name="Test Game",
            url="https://example.com",
            price=10
        )

        # Call the get_absolute_url method
        absolute_url = game.get_absolute_url()

        # Check that the absolute URL is generated correctly
        self.assertEqual(absolute_url, "/game/1")

    def test_game_save_method(self):
        # Create a test game
        game = Game(
            developer=self.user,
            name="Test Game",
            url="https://example.com",
            price=10
        )

        # Save the game
        game.save()

        # Check that the created field is set
        self.assertIsNotNone(game.created)
        self.assertIsInstance(game.created, datetime.datetime)
        self.assertLessEqual(game.created, timezone.now())

    def test_game_tags_field(self):
        # Create a test game
        game = Game.objects.create(
            developer=self.user,
            name="Test Game",
            url="https://example.com",
            price=10
        )

        # Check that the tags field is empty initially
        self.assertEqual(game.tags.count(), 0)

        # Add a tag to the game
        tag = Tag.objects.create(name="Action")
        game.tags.add(tag)

        # Check that the tag is added to the game
        self.assertEqual(game.tags.count(), 1)
        self.assertIn(tag, game.tags.all())
        

class GameStateModelTestCase(TestCase):
    import time

class GameStateModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Create a developer user
        developer = User.objects.create_user(username="testdeveloper", password="testpassword", is_developer=True)

        # Create a game with the developer
        self.game = Game.objects.create(name="Test Game", developer=developer)

    def test_game_state_str_representation(self):
        # No need to create a user here, it's already created in setUp

        # Create a developer user
        developer = User.objects.create_user(username="testdeveloper2", password="testpassword", is_developer=True)

        # Create a game with the developer
        self.game = Game.objects.create(name="Test Game", developer=developer)

    def test_game_state_ordering(self):
        # Create test game states with different dates
        game_state1 = GameState.objects.create(user=self.user, game=self.game, data="Test Data 1")
        time.sleep(1)  # Add a small delay to ensure the dates are different
        game_state2 = GameState.objects.create(user=self.user, game=self.game, data="Test Data 2")

        # Check that the game states are ordered correctly by date
        game_states = GameState.objects.all()
        self.assertEqual(game_states[0], game_state2)
        self.assertEqual(game_states[1], game_state1)
    
    def test_game_state_fields(self):
        # Create a test game state
        game_state = GameState.objects.create(user=self.user, game=self.game, data="Test Data")

        # Check that the fields are set correctly
        self.assertEqual(game_state.user, self.user)
        self.assertEqual(game_state.game, self.game)
        self.assertEqual(game_state.data, "Test Data")
        

class PaymentModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Create a developer user
        developer = User.objects.create_user(username="testdeveloper", password="testpassword", is_developer=True)

        # Create a game with the developer
        self.game = Game.objects.create(name="Test Game", developer=developer, price=Decimal("9.99"))

    def test_payment_str_representation(self):
        # Create a test payment
        payment = Payment.objects.create(user=self.user, game=self.game, amount=Decimal("9.99"))

        # Check that the string representation of the payment is formatted correctly
        expected_str = "{} | {}$ | {}".format(self.game, payment.amount, payment.date.strftime("%Y-%m-%d | %H:%m"))
        self.assertEqual(str(payment), expected_str)

    def test_payment_attributes(self):
        # Create a test payment
        payment = Payment.objects.create(user=self.user, game=self.game, amount=Decimal("9.99"))

        # Check that the payment attributes are set correctly
        self.assertEqual(payment.user, self.user)
        self.assertEqual(payment.game, self.game)
        self.assertEqual(payment.amount, Decimal("9.99"))
        self.assertAlmostEqual(payment.date, timezone.now(), delta=timezone.timedelta(seconds=1))