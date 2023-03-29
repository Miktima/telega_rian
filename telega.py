from telethon.sync import TelegramClient
import json
import time
import datetime

with open('config.json') as json_file:
    confile = json.load(json_file)
    config = confile['init_parameters']
    id = config['id']
    hash = config['hash']
    phone = config['phone']
client = TelegramClient('newsrate', id, hash)

async def main():
    channel_name = "РИА Новости"
    await client.start(phone=phone)
    async for dialog in client.iter_dialogs():
        if dialog.name == channel_name:
            channel = await client.get_entity(dialog.id)
            break
    time.sleep(0)
    flag = True
    it = 0
    while flag:
        mes_dic = {}
        for_order = []
        async for message in client.iter_messages(channel, limit=100):
            td_sec = datetime.timedelta.total_seconds(datetime.datetime.now(tz=datetime.timezone.utc) - message.date)
            vel = message.forwards / td_sec
            mes_dic.update({message.id: [message.message, message.forwards, message.date, vel]})
            for_order.append((message.id, vel))
        order = sorted(for_order, key=lambda tuple: tuple[1], reverse=True)
        print(f'#########################{datetime.datetime.now()}##################################')
        for ord in order[0:5]:
            print(f'ID:{ord[0]}, message: {(mes_dic.get(ord[0]))[0]}, messade date(UTC): {(mes_dic.get(ord[0]))[2]}, rate: {(mes_dic.get(ord[0]))[3]} ')
        print("/n")
        time.sleep(10)
        it += 1
        if it == 10:
            flag = False
        
with client:
    client.loop.run_until_complete(main())