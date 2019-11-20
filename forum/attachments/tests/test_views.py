import os
import shutil

from django.urls import reverse
from django.test import override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from test_plus import TestCase

from forum.attachments.models import Attachment
from forum.accounts.tests.utils import login

TEST_IMAGES_DIR = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'testimages'
)
TEST_IMAGE_1 = os.path.join(TEST_IMAGES_DIR, 'abu3.jpg')
TEST_IMAGE_2 = os.path.join(TEST_IMAGES_DIR, 'aprf1.jpg')
TEST_IMAGE_3 = os.path.join(TEST_IMAGES_DIR, 'Chrysanthemum.jpg')

IMAGE_UPLOAD_DIR = os.path.join(settings.TEST_MEDIA_ROOT, 'uploads')


@override_settings(MEDIA_ROOT=settings.TEST_MEDIA_ROOT)
class ImageUploadViewTest(TestCase):
    def setUp(self):
        self.user = self.make_user('john')
        self.upload_url = reverse('attachments:upload_img')
        self.test_image = SimpleUploadedFile(
            name='abu3.jpg',
            content=open(TEST_IMAGE_1, 'rb').read(),
            content_type='image/jpeg'
        )
        self.test_image2 = SimpleUploadedFile(
            name='aprf1.jpg',
            content=open(TEST_IMAGE_2, 'rb').read(),
            content_type='image/jpeg'
        )
        self.test_image3 = SimpleUploadedFile(
            name='Chrysanthemum.jpg',
            content=open(TEST_IMAGE_3, 'rb').read(),
            content_type='image/jpeg'
        )

    def tearDown(self):
        self.test_image.close()
        self.test_image2.close()

        try:
            if os.path.isdir(settings.TEST_MEDIA_ROOT):
                shutil.rmtree(settings.TEST_MEDIA_ROOT)
        except Exception as e:
            print(e)

    def test_post_with_authenticated_user_without_ajax(self):
        login(self, self.user, 'password')
        data = {'image': self.test_image}
        response = self.client.post(self.upload_url, data)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(Attachment.objects.count(), 0)

    def test_post_with_anonymous_user_with_ajax(self):
        data = {'image': self.test_image}
        response = self.client.post(
            self.upload_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Attachment.objects.count(), 0)

    def test_post_with_authenticated_user_with_ajax(self):
        current_count = Attachment.objects.count()
        login(self, self.user, 'password')
        data = {'image': self.test_image}
        response = self.client.post(
            self.upload_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Attachment.objects.count(), current_count + 1)

    def test_post_with_duplicate_images(self):
        current_count = Attachment.objects.count()
        login(self, self.user, 'password')
        data = {'image': self.test_image}

        first_response = self.client.post(
            self.upload_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEquals(first_response.status_code, 200)

        second_response = self.client.post(
            self.upload_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEquals(second_response.status_code, 200)

        self.assertEquals(Attachment.objects.count(), current_count + 1)
        path, dirs, files = next(os.walk(IMAGE_UPLOAD_DIR))
        self.assertEquals(len(files), 1)

    def test_post_with_two_images(self):
        current_count = Attachment.objects.count()
        login(self, self.user, 'password')

        data = {'image': self.test_image}
        first_response = self.client.post(
            self.upload_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEquals(first_response.status_code, 200)

        data2 = {'image': self.test_image2}
        second_response = self.client.post(
            self.upload_url, data2, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEquals(second_response.status_code, 200)

        self.assertEquals(Attachment.objects.count(), current_count + 2)
        path, dirs, files = next(os.walk(IMAGE_UPLOAD_DIR))
        self.assertEquals(len(files), 2)

    def test_with_empty_data(self):
        login(self, self.user, 'password')
        data = {}
        response = self.client.post(
            self.upload_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEquals(response.status_code, 200)
        self.assertFalse(response.json()['is_valid'])
        self.assertEquals(
            response.json()['message'], 'This field is required.'
        )

    def test_with_invalid_data(self):
        login(self, self.user, 'password')
        data = {'image': ''}
        response = self.client.post(
            self.upload_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEquals(response.status_code, 200)
        attachment_qs = Attachment.objects.filter(image='')
        self.assertFalse(attachment_qs.exists())
        self.assertFalse(response.json()['is_valid'])
        self.assertEquals(
            response.json()['message'], 'This field is required.'
        )

    def test_with_large_image(self):
        login(self, self.user, 'password')
        data = {'image': self.test_image3}
        response = self.client.post(
            self.upload_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Attachment.objects.count(), 0)
        self.assertFalse(response.json()['is_valid'])
        message = 'File too large. Size should not exceed 500 KB.'
        self.assertEquals(response.json()['message'], message)

    def test_with_valid_data(self):
        login(self, self.user, 'password')
        data = {'image': self.test_image}
        response = self.client.post(
            self.upload_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEquals(response.status_code, 200)
        attachment_qs = Attachment.objects.filter(
            image=response.json()['name']
        )
        self.assertTrue(response.json()['is_valid'])
        self.assertTrue(attachment_qs.exists())
