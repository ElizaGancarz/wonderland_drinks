from io import BytesIO

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.testcases import TestCase
from django.utils import timezone

from cocktails.models import Drink, Ingredient, Product, UnitType


class TestDrink(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='test123')
        self.client.login(username='testuser', password='test123')
        self.name = 'testdrink'
        self.time_now = timezone.now()
        self.image = self.create_image_file()
        self.drink = Drink.objects.create(
            name=self.name,
            owner=self.user,
            creation_date=self.time_now,
            image=self.image,
            public=True,
            pin_to_main_page=False,
        )

    def create_image_file(self, name='test.png', size=(50, 50), image_mode='RGB', image_format='JPEG'):
        image = Image.new(image_mode, size)
        buffer = BytesIO()
        image.save(buffer, format=image_format)
        return SimpleUploadedFile(name, buffer.getvalue())

    def test_drink_created_correctly(self):
        drink_from_db = Drink.objects.get(name=self.name)
        self.assertEqual(drink_from_db.name, self.drink.name)
        self.assertEqual(drink_from_db.owner, self.drink.owner)
        self.assertEqual(drink_from_db.creation_date, self.drink.creation_date)
        self.assertEqual(drink_from_db.public, self.drink.public)
        self.assertEqual(drink_from_db.pin_to_main_page, self.drink.pin_to_main_page)
        self.assertEqual(drink_from_db.likes, 0)

        drinks = Drink.objects.all()
        self.assertEqual(drinks.count(), 1)

    def test_ingredients_property(self):
        product = Product.objects.create(name='testproduct')
        unit_type = UnitType.objects.create(name='testunit', short_name='TU')
        ingredient_amount = 2

        Ingredient.objects.create(
            product=product,
            unit=unit_type,
            amount=ingredient_amount,
            drink=self.drink
        )

        drink_from_db = Drink.objects.get(name=self.name)

        self.assertEqual(drink_from_db.ingredients.count(), 1)

    def test_duplicated_drink_name(self):
        drink = Drink.objects.create(
            name=self.name,
            owner=self.user,
            creation_date=self.time_now,
            image=self.image,
            public=True,
            pin_to_main_page=False,
        )

        self.assertRaises(Exception, drink.full_clean)

    def test_drink_with_too_long_name(self):
        drink = Drink.objects.create(
            name='a' * 101,
            owner=self.user,
            creation_date=self.time_now,
            image=self.image,
            public=True,
            pin_to_main_page=False,
        )

        self.assertRaises(Exception, drink.full_clean)

    def test_drink_with_too_long_description(self):
        drink = Drink.objects.create(
            name=self.name,
            owner=self.user,
            creation_date=self.time_now,
            image=self.image,
            description='a' * 501,
            public=True,
            pin_to_main_page=False,
        )

        self.assertRaises(Exception, drink.full_clean)

    def test_drink_with_blank_name(self):
        drink = Drink.objects.create(
            name='',
            owner=self.user,
            creation_date=self.time_now,
            image=self.image,
            public=True,
            pin_to_main_page=False,
        )

        self.assertRaises(Exception, drink.full_clean)