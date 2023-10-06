from io import BytesIO

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from cocktails.models import Drink


class CocktailsViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='test123')
        self.client.login(username='testuser', password='test123')
        self.name = 'testdrink'
        self.image = self.create_image_file()
        self.drink = Drink.objects.create(
            name=self.name,
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

    def test_dashboard_view_when_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_dashboard_view_when_not_login(self):
        self.client.logout()
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/login/?next=/dashboard/', status_code=302, target_status_code=200)

    def test_create_drink_view_when_login(self):
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create.html')

    def test_create_drink_view_when_not_login(self):
        self.client.logout()
        response = self.client.get(reverse('create'))
        self.assertRedirects(response, '/login/?next=/dashboard/create/', status_code=302, target_status_code=200)

    def test_edit_drink_view(self):
        response = self.client.get(reverse('edit', args=[self.drink.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create.html')

    def test_edit_drink_view_when_not_login(self):
        self.client.logout()
        response = self.client.get(reverse('edit', args=[self.drink.id]))
        self.assertRedirects(response, '/login/?next=/dashboard/edit/1/', status_code=302, target_status_code=200)

    def test_delete_drink_view(self):
        response = self.client.post(reverse('delete_drink', args=[self.drink.id]))
        self.assertRedirects(response, reverse('dashboard'))
        self.assertFalse(Drink.objects.filter(id=self.drink.id).exists())

    def test_delete_drink_view_when_not_login(self):
        self.client.logout()
        response = self.client.get(reverse('delete_drink', args=[self.drink.id]))
        self.assertRedirects(response, '/login/?next=/dashboard/delete_drink/1/', status_code=302,
                             target_status_code=200)
