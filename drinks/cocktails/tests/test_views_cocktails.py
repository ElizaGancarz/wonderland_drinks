from io import BytesIO

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.testcases import TestCase
from django.urls import reverse
from django.utils import timezone

from cocktails.models import Drink


class TestCocktails(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='test123')
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

    def test_home_view_correctly_display_when_not_login(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_view_correctly_display_when_login(self):
        self.client.login(username='testuser', password='test123456')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_search_view(self):
        response = self.client.get(reverse('search') + '?q=Test')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_results.html')

    def test_detail_cocktail_view(self):
        response = self.client.get(reverse('detail_cocktail', args=[self.drink.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cocktail_detail.html')
