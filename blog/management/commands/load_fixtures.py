from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        call_command("makemigrations")
        call_command("migrate")
        call_command("loaddata", "article_data.json")
        call_command("loaddata", "category_data.json")
        call_command("loaddata", "users_data.json")
