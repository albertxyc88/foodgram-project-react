import json
import os

from django.conf import settings
from django.core.management import BaseCommand
from recipe.models import Ingredients

ingredients_file = open(
    os.path.join(
        settings.BASE_DIR,
        '../data/ingredients.json',
    ),
    encoding='utf-8'
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--ingredients',
            type=str,
            nargs='?',
            help='Загрузка данных в базу данных из файла ingredients.json'
        )

    def handle(self, *args, **options):
        # Если данные не пустые повторно не загружаем.
        if Ingredients.objects.exists():
            print('Данные в ingredients уже загружены. Аварийное завершение.')
        else:
            print('Загрузка данных в ingredients.')
            data = json.load(ingredients_file)
            for element in data:
                Ingredients.objects.create(name=element['name'],
                    measurement_unit = element['measurement_unit']
                )
            print('Загрузка данных в ingredients завершена.')