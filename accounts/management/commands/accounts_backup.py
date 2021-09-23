import csv
import datetime
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from accounts.models import Users


class Command(BaseCommand):
    def handle(self, *args, **options):

        date = datetime.date.today().strftime("%Y%m%d")

        file_path = settings.BACKUP_PATH + 'Users_' + date + '.csv'

        os.makedirs(settings.BACKUP_PATH, exist_ok=True)

        with open(file_path, 'w') as file:
            writer = csv.writer(file)

            header = [field.name for field in Users._meta.fields]
            writer.writerow(header)

            users_object = Users.objects.all()

            for user in users_object:
                writer.writerow([
                    user.id,
                    user.password,
                    user.last_login,
                    user.is_superuser,
                    user.username,
                    user.signature,
                    user.email,
                    user.is_staff,
                    user.is_active,
                    user.date_joined
                ])
