import django
import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poker_with_friends.settings')
django.setup()

from apscheduler.schedulers.blocking import BlockingScheduler
from poker.models import Table, SavedTable
from datetime import datetime

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print(datetime.now() + "\n", "Running cronjob...\n\n")
    for table in Table.objects.all():
        time1 = datetime.now()
        time2 = table.date
        elapsedTime = time2 - time1
        print(time1 + "  ", time2, ":  ", elapsedTime, "\n\n")
        
        if elapsedTime.total_seconds() > 3600 and (table.player1 == "none" or table.player2 == "none"):
            table.delete()
            saved_table = SavedTable(table_name=table.table_name, player1=table.player1, player2=table.player2, date=table.date, access_code=table.access_code)
            saved_table.save()
            
        elif elapsedTime.total_seconds() > 3600:
            table.delete()
            saved_table = SavedTable(table_name=table.table_name, player1=table.player1, player2=table.player2, date=table.date, access_code=table.access_code)
            saved_table.save()

'''@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')'''

sched.start()