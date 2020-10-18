from django.core.management.base import BaseCommand
from customers.models import Plan
import csv
from datetime import datetime

class Command(BaseCommand):
    help = 'Imports the customer plan input csv'


    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str)


    def handle(self, *args, **options):

        filename = options['filename'][0]

        with open('./customers/data/' + filename, newline='') as csvfile:
            plan_reader = csv.reader(csvfile, delimiter=',')
            header = True
            for row in plan_reader:
                if (header):
                    header = False
                    continue

                user_id = row[0]
                storage_plan=row[2]
                try:
                    start_date = format_input_date(row[1])
                    end_date=format_input_date(row[3])
                except Exception as e:
                    self.stdout.write("Could not format date. Skipping row: " + str(row) + " " + str(e))
                    continue

                plan = Plan.objects.create(user_id=user_id, start_date=start_date, storage_plan=storage_plan, end_date=end_date)
                plan.save()

            self.stdout.write(self.style.SUCCESS('Successfully populated Plan table'))


def format_input_date(input_date):

    if (input_date and len(input_date) > 0):
        date_object = datetime.strptime(input_date, '%b %d, %Y')
        output_date = date_object.strftime('%Y-%m-%d')
        #print ("INPUT: " + str(input_date) +  " OUTPUT: " + str(output_date))
        return output_date
    else:
        return None