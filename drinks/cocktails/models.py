import random
import string
import os

from PIL import Image
from io import BytesIO
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


def random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


class Product(models.Model):
    name = models.CharField(max_length=220, unique=True)

    def __str__(self):
        return self.name


class UnitType(models.Model):
    name = models.CharField(max_length=20)
    short_name = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.name} [{self.short_name}]'


class Drink(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    public = models.BooleanField(default=True)
    pin_to_main_page = models.BooleanField(default=False)
    likes = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} | {self.creation_date} | {self.description}'

    @property
    def ingredients(self):
        return Ingredient.objects.filter(drink=self)

    def is_liked_by_user(self, user):
        return self.like_set.filter(user=user).exists()

    def update_like_count(self):
        self.likes = Like.objects.filter(drink=self).count()
        self.save()

    def save(self, *args, **kwargs):

        self.thumbnail = self.create_thumbnail()
        super(Drink, self).save(*args, **kwargs)

    def create_thumbnail(self):
        image = Image.open(self.image)
        max_size = (300, 200)

        if image.width > max_size[0] or image.height > max_size[1]:
            image.thumbnail(max_size, Image.LANCZOS)

        thumbnail_io = BytesIO()
        image.save(thumbnail_io, 'JPEG', quality=85)

        thumbnail_filename = random_string(10) + '.jpg'

        thumbnail_path = thumbnail_filename
        self.thumbnail.save(thumbnail_path,
                            InMemoryUploadedFile(thumbnail_io, None, thumbnail_path, 'image/jpeg',
                                                 thumbnail_io.tell(), None), save=False)

        return self.thumbnail


class Ingredient(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
    )
    unit = models.ForeignKey(
        UnitType,
        on_delete=models.SET_NULL,
        null=True,
    )
    amount = models.PositiveIntegerField(default=1)
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.drink.name}  | {self.product.name}  |  {self.amount} {self.unit.short_name}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
