import sys
sys.path.insert(0, 'J:/scheduler/')

from scheduler import get_full_schedule
from datetime import datetime, timedelta
today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) 
tomorrow = today + timedelta(days=1)

events = get_full_schedule('J:/scheduler/events', tomorrow)

now = datetime.now().replace(minute=0, second=0, microsecond=0)
hour = timedelta(hours=1)
while now < tomorrow:
    print now.strftime('%H:%M'),

    if events[0].start_date < now + hour:
        print events[0].name
    else:
        print '-'

    if events[0].end_date < now + hour:
        now = events.pop(0).end_date
    else:
        now = now.replace(minute=0, second=0, microsecond=0) + hour

raw_input()
