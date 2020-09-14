from django.core.management.base import BaseCommand, CommandError
from poker.models import Table, SavedTable
from datetime import datetime
import pytz
utc=pytz.UTC

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("heheieife")
        self.stdout.write("Running cronjob...\n\n")
        #self.stdout.write(Table.objects.all())
        for table in Table.objects.all():
            #self.stdout.write("hereee")
            print(Table)
            time1 = datetime.now()
            time1 = utc.localize(time1)
            time2 = table.date
            elapsedTime = time1 - time2
            #self.stdout.write(time1, "  ", time2, ":  ", elapsedTime," ", elapsedTime.days, " ", elapsedTime.seconds,  "\n\n")
            
            if elapsedTime.days > 0:
                self.stdout.write("deleting1..")    
                saved_table = SavedTable(table_name=table.table_name, player1=table.player1, player2=table.player2, date=table.date, access_code=table.access_code)
                saved_table.save()
                table.delete()
            elif elapsedTime.seconds > 3600 and table.player1 == "none" and table.player2 == "none":
                self.stdout.write("deleting2..")
                saved_table = SavedTable(table_name=table.table_name, player1=table.player1, player2=table.player2, date=table.date, access_code=table.access_code)
                saved_table.save()
                table.delete()

#from apscheduler.schedulers.blocking import BlockingScheduler
#from poker.models import Table, SavedTable
#from datetime import datetime
#import pytz
#utc=pytz.UTC
'''sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print(datetime.now(), "\n", "Running cronjob...\n\n")
    print(Table.objects.all())
    for table in Table.objects.all():
        print("hereee")
        time1 = datetime.now()
        time1 = utc.localize(time1)
        time2 = table.date
        elapsedTime = time1 - time2
        print(time1, "  ", time2, ":  ", elapsedTime," ", elapsedTime.days, " ", elapsedTime.seconds,  "\n\n")

        if elapsedTime.days > 0:
            print("here1")
            saved_table = SavedTable(table_name=table.table_name, player1=table.player1, player2=table.player2, date=table.date, access_code=table.access_code)
            saved_table.save()
            table.delete()
        elif elapsedTime.seconds > 3600 and table.player1 == "" and table.player2 == "":
            print("here2")
            saved_table = SavedTable(table_name=table.table_name, player1=table.player1, player2=table.player2, date=table.date, access_code=table.access_code)
            saved_table.save()
            table.delete()'''
