from django.test import TestCase
from gamestore.models import User, Tag, Game, Payment
from decimal import Decimal
from django.utils import timezone
import datetime

class UserModelTestCase(TestCase):
    def test_user_str_representation(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        self.assertEqual(str(user), "testuser")

    def test_user_is_developer_default_value(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        self.assertFalse(user.is_developer)

    def test_user_get_token(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        token = user.get_token()
        self.assertIsInstance(token, str)


class TagModelTestCase(TestCase):
    def test_tag_str_representation(self):
        tag = Tag(name="testtag")
        self.assertEqual(str(tag), "testtag")


class GameModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_game_str_representation(self):
        game = Game.objects.create(
            developer=self.user,
            name="Test Game",
            url="https://example.com",
            price=10
        )
        self.assertEqual(str(game), "Test Game")

    def test_game_get_absolute_url(self):
        game = Game.objects.create(
            developer=self.user,
            name="Test Game",
            url="https://example.com",
            price=10
        )
        absolute_url = game.get_absolute_url()
        self.assertEqual(absolute_url, "/game/1")

    def test_game_save_method(self):
        game = Game(
            developer=self.user,
            name="Test Game",
            url="https://example.com",
            price=10
        )
        game.save()
        self.assertIsNotNone(game.created)
        self.assertIsInstance(game.created, datetime.datetime)
        self.assertLessEqual(game.created, timezone.now())

    def test_game_tags_field(self):
        game = Game.objects.create(
            developer=self.user,
            name="Test Game",
            url="https://example.com",
            price=10
        )
        self.assertEqual(game.tags.count(), 0)
        tag = Tag.objects.create(name="Action")
        game.tags.add(tag)
        self.assertEqual(game.tags.count(), 1)
        self.assertIn(tag, game.tags.all())
