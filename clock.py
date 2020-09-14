'''import django
import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poker_with_friends.settings')
django.setup()

from apscheduler.schedulers.blocking import BlockingScheduler
from poker.models import Table, SavedTable
from datetime import datetime
import pytz
utc=pytz.UTC
'''
sched = BlockingScheduler()

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
            table.delete()

'''@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')'''

#sched.start()
