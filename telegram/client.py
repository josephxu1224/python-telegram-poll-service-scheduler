# -*- coding: utf-8 -*-
import asyncio
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import SessionPasswordNeededError
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, MessageMediaDocument, DocumentAttributeAudio, MessageMediaWebPage, \
    WebPage, WebPageEmpty,InputMediaPoll, Poll, PollAnswer,MessageMediaPoll
import csv,sys
import datetime
from pytz import timezone


class Client:
    @staticmethod
    def is_number(n):
        try:
            int(n)
        except ValueError:
            return False
        return True

    def __init__(self):
        self.api_id = 941748
        self.client_id = 821608836
        self.admin_id = 460150389
        self.api_hash = '03398ae66b58de459de3ed8a67adea40'
        self.phone = '+14155219187'
        self.client = TelegramClient(self.phone, self.api_id, self.api_hash)
        self.current_date = datetime.datetime.now().strftime("%Y%m%d")
        self.available_groups = {}

    async def connect(self):
        await self.client.connect()
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone)
            try:
                await self.client.sign_in(self.phone, input('Enter the code: '))
            except SessionPasswordNeededError:
                await self.client.sign_in(password=input('Password: '))
        self.available_groups = await self.retrieve_group_chat_list()
    async def retrieve_group_chat_list(self):
        chats = []
        last_date = None
        chunk_size = 2000
        groups = {}
        result = await self.client(GetDialogsRequest(
            offset_date=last_date,
            offset_id=-0,
            offset_peer=InputPeerEmpty(),
            limit=chunk_size,
            hash=0
        ))
        chats.extend(result.chats)
        for chat in chats:
            try:
                groups[chat.id] = chat.title
            except Exception as e:
                print(e)
                continue
        return groups
    async def print_groups_info(self, group_name=None, save_file=True):
        chats = []
        titles = []
        last_date = None
        chunk_size = 2000
        groups = []
        result = await self.client(GetDialogsRequest(
            offset_date=last_date,
            offset_id=-0,
            offset_peer=InputPeerEmpty(),
            limit=chunk_size,
            hash=0
        ))
        chats.extend(result.chats)
        for chat in chats:
            try:
                # print(chat.title)
                # if chat.megagroup:
                groups.append(chat)
                titles.append(chat.title)
            except Exception as e:
                print(e)
                continue
        # groups = list(set(groups))
        if not group_name:
            print('Choose a group to scrape members from:')
            i = 0
            for g in groups:
                print(str(i) + '- ' + g.title + '-' + str(g.id))
                i += 1
            g_index = input("Enter a Number: ")
            target_group = groups[int(g_index)]

        else:
            try:
                g_index = titles.index(group_name)
            except Exception as e:
                print(str(e))
                target_group = None
            else:
                target_group = groups[g_index]
        #await self.export_members_info_in_group(target_group)
    async def get_input_entity(self, entity_id):
        entity = await self.client.get_input_entity(entity_id)
        return entity
    async def print_group_messages(self,entity):
        async for message in self.client.iter_messages(entity):
            if(message.message):
                contents = message.message.split("\n\n")
                if len(contents)==3:
                    print(contents)
    async def export_members_info_in_group(self, target_group):
        if target_group:
            print('Fetching Members...')
            all_participants = await self.client.get_participants(target_group, aggressive=True)
            all_participants_ids = {}
            all_participants_info = []
            for user in all_participants:
                if user.username:
                    username = user.username
                else:
                    username = ""
                if user.first_name:
                    first_name = user.first_name
                else:
                    first_name = ""
                if user.last_name:
                    last_name = user.last_name
                else:
                    last_name = ""
                name = (first_name + ' ' + last_name).strip()
                all_participants_ids["{}".format(name)] = user.id
                participant_info = [name, user.id, user.access_hash, username, target_group.title, target_group.id]
                all_participants_info.append(participant_info)
            print('Saving In file...')
            with open("{}-members.csv".format(target_group.title.replace("/", "-")), "w",
                      encoding='UTF-8') as f:
                writer = csv.writer(f, delimiter=",", lineterminator="\n")
                writer.writerow(['Name', 'UserId', 'AccessHash', 'UserName', 'group', 'group id'])
                for participant_info in all_participants_info:
                    writer.writerow(participant_info)
            print('Members scraped successfully.')
            return all_participants_ids
        else:
            raise TypeError("Please check your group name")
    async def send_poll(self,target_group):
        #target_group = await self.get_input_entity(group_id)
        poll_id = int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"));
        weekday = datetime.datetime.today().weekday();
        hour = int(datetime.datetime.now().strftime("%H"));
        if(hour < 12):
            poll_date = datetime.datetime.now().strftime("%m/%d(%A)");
            service = "Morning Service"
        else:
            poll_date = datetime.datetime.now().strftime("%m/%d");
            if weekday == 2:
                service = "Wednesday Service"
            elif weekday == 4:
                service = "Friday Prayer Service"
            elif weekday == 6:
                service = "Sunday Service"
            else:
                service = "Bible Study"
                poll_date = datetime.datetime.now().strftime("%m/%d (%A) ");
        poll_title = 'Did you attend {} {}?'.format(poll_date, service)

        message = await self.client.send_message(target_group, file=InputMediaPoll(
                poll=Poll(
                    id = poll_id,
                    question= poll_title,
                    answers=[PollAnswer('Yes', b'1'), PollAnswer('No', b'0')],
                    public_voters = True
                )
        ))
        await self.client.pin_message(target_group, message, notify=True)
    async def remind_poll(self, group_id):
        target_group = await self.get_input_entity(group_id)
        async for message in self.client.iter_messages(target_group):
            message_created_date = message.date.astimezone(timezone('America/Los_Angeles'))
            message_created_date_str = message_created_date.strftime("%Y%m%d")
            if(message_created_date_str < self.current_date):
                break;
            if isinstance(message.media, MessageMediaPoll):
                if not message.media.poll.closed:
                    if(not message.pinned):
                        await self.client.pin_message(target_group, message, notify=True)
                    break
    async def stop_poll(self, group_id):
        target_group = await self.get_input_entity(group_id)
        async for message in self.client.iter_messages(target_group):
            message_created_date = message.date.astimezone(timezone('America/Los_Angeles'))
            message_created_date_str = message_created_date.strftime("%Y%m%d")
            if(message_created_date_str < self.current_date):
                break;
            if isinstance(message.media, MessageMediaPoll):
                if not message.media.poll.closed:
                    message.media.poll.closed = True
                    edited_poll = message.media.poll
                    try:
                        await self.client.edit_message(target_group, message.id, file=InputMediaPoll(
                            poll=edited_poll
                        ));
                    except Exception as e:
                        print(e)
                    else:
                        print("Stop poll successfully!")
                        await self.client.unpin_message(target_group, message)
                        break
    async def schedule_poll(self, group_id):
        target_group = await self.get_input_entity(group_id)
        is_sent = False
        async for message in self.client.iter_messages(target_group):
            message_created_date = message.date.astimezone(timezone('America/Los_Angeles'))
            message_created_date_str = message_created_date.strftime("%Y%m%d")
            if(message_created_date_str < self.current_date):
                break;
            if isinstance(message.media, MessageMediaPoll):
                if not message.media.poll.closed:
                    is_sent = True
                    break
        if not is_sent:
            await self.send_poll(target_group)
        else:
            print("There has been a available poll sent!")
