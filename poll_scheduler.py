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
