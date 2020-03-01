from django.urls import reverse

from test_plus import TestCase
from faker import Faker

from forum.categories.models import Category, CategoryQuerySet

fake = Faker()


class CategoryModelTest(TestCase):
    def setUp(self):
        self.user = self.make_user('testuser1')
        self.category = Category.objects.create(
            title='progromming group',
            description='NA'
        )

    def test_save(self):
        cat = Category(title='Test Title', description='Test description')
        cat.save()
        self.assertEquals(cat.slug, 'test-title')


class CategoryModelManagerTest(CategoryModelTest):
    def test_get_by_slug(self):
        category = Category.objects.get_by_slug(self.category.slug)
        self.assertEquals(category, self.category)
