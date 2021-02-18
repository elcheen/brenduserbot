# Copyright (C) 2021 ᴇʟçɪɴ ¦ 🇯🇵
#
# Licensed under the GPL-3.0 License;
# you may not use this file except in compliance with the License.
#

# Brend UserBot - ᴇʟçɪɴ ¦ 🇯🇵

from userbot.events import register
from eksipy import Baslik, Giri, Eksi
from datetime import datetime
import urllib.parse
from userbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern="^.başlıq(\d*) ?(.*)")
async def baslik(event):
    səhifə = event.pattern_match.group(1)
    if səhifə == '':
        səhifə = 1
    else:
        səhifə = int(sayfa)

    başlıq = event.pattern_match.group(2)
    try:
        başlıq = Başlıq(başlıq, səhifə)
    except:
        return await event.edit('`Belə bir başlıq tapılmadı.`')
    
    topic = başlıq.get_topic()
    entrys = başlıq.get_entrys()
    Result = f'**Başlıq: **`{topic.title}`\n`{topic.current_page}/{topic.max_page}`\n\n'
    
    for entry in entrys:
        if len(entry.text().strip()) < 450:
            Result += f'`{entry.text().strip()}`\n__[{datetime.utcfromtimestamp(entry.date).strftime("%d/%m/%Y")}](https://eksisozluk.com/entry/{entry.id}) [{entry.author}](https://eksisozluk.com/biri/{urllib.parse.quote(entry.author)})__\n\n'
        else:
            Result += f'**Bu entry uzun görünür.** `.entry {entry.id}` ile ala bilərsiniz.\n\n'
    return await event.edit(Result)

@register(outgoing=True, pattern="^.entry ?(\d*)")
async def entry(event):
    Entry = int(event.pattern_match.group(1))
    try:
        Entry = Giri(Entry).get_entry()
    except:
        return await event.edit('`Belə bir entry tapılmadı.`')
    
    Result = f'**Başlıq: **`{Entry.topic.title}`\n\n'
    Result += f'`{Entry.text().strip()}`\n __[{datetime.utcfromtimestamp(Entry.date).strftime("%d/%m/%Y")}](https://eksisozluk.com/entry/{Entry.id}) [{Entry.author}](https://eksisozluk.com/biri/{urllib.parse.quote(Entry.author)})__\n\n'
    return await event.edit(Result)

@register(outgoing=True, pattern="^.g[üu]ndəm ?(\d*)$")
async def gundəm(event):
    if event.pattern_match.group(1) == '':
        Səhifə = 1
    else:
        Səhifə = int(event.pattern_match.group(1))

    try:
        Gündəm = Eksi().gundem(Səhifə)
    except:
        return await event.edit('`Bir xəta baş verdi.`')
    
    Result = ""
    i = 1
    for Baslik in Gundem:
        Result += f'`{i}-)` [{Başlıq.title}]({Başlıq.url()}) __{Başlıq.giri}__\n'
    return await event.edit(Result)

CmdHelp('köhnə').add_command(
    'başlıq', '<səhifə> <başlıq', 'Ekşi Sözlükte başlıq gətirər.', 'başlıq2 php'
).add_command(
    'entry', '<id>', 'Entry gətirər.', 'entry 1'
).add_command(
    'gundem', '<səhifə'>, 'Gündəm gətirər.', 'gündəm 1'
).add()
