import csv
import datetime
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from client.models import Clients


class Command(BaseCommand):
    def handle(self, *args, **options):

        date = datetime.date.today().strftime("%Y%m%d")

        file_path = settings.BACKUP_PATH + 'Clients_' + date + '.csv'

        os.makedirs(settings.BACKUP_PATH, exist_ok=True)

        with open(file_path, 'w') as file:
            writer = csv.writer(file)

            header = [field.name for field in Clients._meta.fields]
            writer.writerow(header)

            clients_object = Clients.objects.all()

            for client in clients_object:
                writer.writerow([
                    client.client_id,
                    client.name,
                    client.name_kana,
                    client.department,
                    client.industry,
                    client.capital,
                    client.postcode,
                    client.address,
                    client.phone_number,
                    client.email,
                    client.fax_number,
                    client.updated_datetime,
                    client.revenue,
                    client.profit,
                    client.number_of_employees,
                    client.remark,
                    client.is_active
                ])
