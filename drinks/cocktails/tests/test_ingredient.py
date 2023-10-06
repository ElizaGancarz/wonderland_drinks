from io import BytesIO

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from cocktails.models import Ingredient, Product, UnitType, Drink


class IngredientModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='test123')
        self.product = Product.objects.create(name='testproduct')
        self.unit_type = UnitType.objects.create(name='testunit', short_name='TU')
        self.image = self.create_image_file()
        self.drink = Drink.objects.create(
            name='testdrink',
            owner=self.user,
            image=self.image,
            public=True,
            pin_to_main_page=False,
        )

    def create_image_file(self, name='test.png', size=(50, 50), image_mode='RGB', image_format='JPEG'):
        image = Image.new(image_mode, size)
        buffer = BytesIO()
        image.save(buffer, format=image_format)
        return SimpleUploadedFile(name, buffer.getvalue())

    def test_create_ingredient(self):
        ingredient = Ingredient.objects.create(
            product=self.product,
            unit=self.unit_type,
            amount=2,
            drink=self.drink
        )
        self.assertEqual(ingredient.product, self.product)
        self.assertEqual(ingredient.unit, self.unit_type)
        self.assertEqual(ingredient.amount, 2)
        self.assertEqual(ingredient.drink, self.drink)

        ingredients = Ingredient.objects.all()
        self.assertEqual(ingredients.count(), 1)

    def test_ingredient_related_drink(self):
        ingredient = Ingredient.objects.create(
            product=self.product,
            unit=self.unit_type,
            amount=2,
            drink=self.drink
        )
        self.assertEqual(ingredient.drink, self.drink)

    def test_ingredient_related_to_product(self):
        ingredient = Ingredient.objects.create(
            product=self.product,
            unit=self.unit_type,
            amount=2,
            drink=self.drink
        )
        self.assertEqual(ingredient.product, self.product)
        self.assertEqual(list(self.product.ingredient_set.all()), [ingredient])

    def test_ingredient_related_unit_type(self):
        ingredient = Ingredient.objects.create(
            product=self.product,
            unit=self.unit_type,
            amount=2,
            drink=self.drink
        )
        self.assertEqual(ingredient.unit, self.unit_type)
        self.assertEqual(list(self.unit_type.ingredient_set.all()), [ingredient])
