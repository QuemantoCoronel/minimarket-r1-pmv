from django.test import TestCase

from .models import Category


class CategoryTests(TestCase):
    def test_name_normalization_is_persisted(self) -> None:
        category = Category.objects.create(name=" Productos Enlatados ")
        self.assertEqual(category.name_normalized, "productos enlatados")

