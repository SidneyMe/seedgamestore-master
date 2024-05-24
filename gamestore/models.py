from cloudinary import models as cloudinary_models
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin, EmailAddress


class User(SimpleEmailConfirmationUserMixin, AbstractUser):
    is_developer = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def get_token(self):
        try:
            email = EmailAddress.objects.get(user=self)
        except EmailAddress.DoesNotExist:
            key = EmailAddress._default_manager.generate_key()
            email = EmailAddress.objects.create(user=self, key=key)
        return str(email.key)


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Game(models.Model):
    developer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    url = models.URLField()
    cover = cloudinary_models.CloudinaryField("cover", blank=True)
    price = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Tags")
    created = models.DateTimeField(editable=False)

    def get_absolute_url(self):
        return reverse('game', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(Game, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    stripe_charge_id = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return "{} | {}$ | {}".format(self.game, self.amount, self.date.strftime("%Y-%m-%d | %H:%m"))
