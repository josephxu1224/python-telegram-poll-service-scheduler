# -*- coding: utf-8 -*-
import argparse
import asyncio
from telegram.client import Client


async def poll_scheduler(group_id, tag='',duration=7):
    client = Client()
    await client.connect()
    if tag == "send":
        await client.schedule_poll(group_id)
    elif tag == "remind":
        await client.remind_poll(group_id)
    elif tag == "stop":
        await client.stop_poll(group_id)
    elif tag == "report":
        print("It is ready to develop......")
        pass
    else:
        await client.print_groups_info()

parser = argparse.ArgumentParser(description='manual to schedule poll')
parser.add_argument('--group-id', type=int, default=0)
parser.add_argument('--tag', type=str, default='')
parser.add_argument('--duration', type=int, default=7)
args = parser.parse_args()
group_id = args.group_id
tag = args.tag
duration = args.duration
if (tag and group_id) or (not tag and not group_id):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(poll_scheduler(group_id, tag, duration))
else:
    print("The arguments - group id and tag should appear at the same time!")

#group_id = 586242376
#group_id = 501560267

# Morning Service Monday to Friday
# 0,30 4 * * 1-5 python3 ~/ScheduleServicePoll/poll_scheduler.py --group-id=586242376 --tag='send'
# 0 6 * * 1-5 python3 ~/ScheduleServicePoll/poll_scheduler.py --group-id=586242376 --tag='remind'
# 30 6 * * 1-5 python3 ~/ScheduleServicePoll/poll_scheduler.py --group-id=586242376 --tag='stop'

# # Wednesday Service and Friday Prayer Meeting
# 30,50 17 * * 3,5 python3 ~/ScheduleServicePoll/poll_scheduler.py --group-id=586242376 --tag='send'
# 30 20 * * 3,5 python3 ~/ScheduleServicePoll/poll_scheduler.py --group-id=586242376 --tag='remind'
# 0 21 * * 3,5 python3 ~/ScheduleServicePoll/poll_scheduler.py --group-id=586242376 --tag='stop'

# # Sunday Service
# 0,30 8 * * 0 python3 ~/ScheduleServicePoll/poll_scheduler.py --group-id=586242376 --tag='send'
# 0 11 * * 0 python3 ~/ScheduleServicePoll/poll_scheduler.py --group-id=586242376 --tag='remind'
# 30 11 * * 0 python3 ~/ScheduleServicePoll/poll_scheduler.py --group-id=586242376 --tag='stop'

