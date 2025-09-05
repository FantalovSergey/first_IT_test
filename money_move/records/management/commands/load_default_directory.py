import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from records.models import Category, Status, Subcategory, Type

CSV_DIR = settings.BASE_DIR / 'directory'


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.load_statuses_and_types(
            (
                ('statuses.csv', Status),
                ('types.csv', Type),
            )
        )
        self.load_categories('categories.csv')
        self.load_subcategories('subcategories.csv')

    def load_statuses_and_types(self, filenames__models_classes):
        for filename, model_class in filenames__models_classes:
            with open(
                file=CSV_DIR / filename, mode='r', encoding='utf-8',
            ) as opened_file:
                try:
                    objects_to_insert = [
                        model_class(name=row['name'])
                        for row in csv.DictReader(opened_file)
                    ]
                except KeyError as field:
                    raise ValueError(
                        f'В файле {filename} отсутствует поле {field}.'
                    )
            model_class.objects.bulk_create(
                objects_to_insert, ignore_conflicts=True,
            )

    def load_categories(self, filename):
        with open(
            file=CSV_DIR / filename, mode='r', encoding='utf-8',
        ) as opened_file:
            types = Type.objects.all()
            categories_to_insert = []
            for row in csv.DictReader(opened_file):
                try:
                    categories_to_insert.append(
                        Category(
                            name=row['name'],
                            type=types.get(name=row['type']),
                        )
                    )
                except KeyError as field:
                    raise ValueError(
                        f'В файле {filename} отсутствует поле {field}.'
                    )
                except Type.DoesNotExist:
                    raise ValueError(
                        f'Ошибка при создании категории {row['name']}: '
                        f'в базе данных отсутствует тип {row['type']}.'
                    )
        Category.objects.bulk_create(
            categories_to_insert, ignore_conflicts=True,
        )

    def load_subcategories(self, filename):
        with open(
            file=CSV_DIR / filename, mode='r', encoding='utf-8',
        ) as opened_file:
            categories = Category.objects.all()
            subcategories_to_insert = []
            for row in csv.DictReader(opened_file):
                try:
                    subcategories_to_insert.append(
                        Subcategory(
                            name=row['name'],
                            category=categories.get(name=row['category']),
                        )
                    )
                except KeyError as field:
                    raise ValueError(
                        f'В файле {filename} отсутствует поле {field}.'
                    )
                except Category.DoesNotExist:
                    raise ValueError(
                        f'Ошибка при создании подкатегории {row['name']}: '
                        'в базе данных отсутствует '
                        f'категория {row['category']}.'
                    )
        Subcategory.objects.bulk_create(
            subcategories_to_insert, ignore_conflicts=True,
        )
