# Copyright (C) 2021 ᴇʟçɪɴ ¦ 🇯🇵
#
# Licensed under the  GPL-3.0 License;
# you may not use this file except in compliance with the License.
#

#Brend UserBot - ᴇʟçɪɴ ¦ 🇯🇵

from userbot.cmdhelp import CmdHelp
from userbot import PLUGIN_CHANNEL_ID, CMD_HELP
from userbot.events import register
from re import search
from json import loads, JSONDecodeError
from userbot.language import LANGUAGE_JSON
from os import remove

@register(outgoing=True, pattern="^.dil ?(.*)")
@register(outgoing=True, pattern="^.lang ?(.*)")
async def dil(event):
    global LANGUAGE_JSON

    əmr = event.pattern_match.group(1)
    if search(r"y[uü]klə|install", əmr):
        await event.edit("`Dil faylı yüklənir... Xahiş olunur gözləyin.`")
        if event.is_reply:
            reply = await event.get_reply_message()
            dosya = await reply.download_media()

            if ((len(reply.file.name.split(".")) >= 2) and (not reply.file.name.split(".")[1] == "brendjson")):
                return await event.edit("`Xahiş olunur düzgün` **BrendJSON** `faylı verin!`")

            try:
                fayl = loads(open(dosya, "r").read())
            except JSONDecodeError:
                return await event.edit("`Xahiş olunur düzgün` **BrendJSON** `faylı verin`")

            await event.edit(f"`{fayl['LANGUAGE']}` `dili yüklənir...`")
            pchannel = await event.client.get_entity(PLUGIN_CHANNEL_ID)

            fayl = await reply.download_media(file="./userbot/language/")
            fayl = loads(open(fayl, "r").read())
            await reply.forward_to(pchannel)
            
            LANGUAGE_JSON = fayl
            await event.edit(f"✅ `{fayl['LANGUAGE']}` `dili uğurla yükləndi!`\n\n**İşlərin uğurlu olması üçün botu yenidən başladın!**")
        else:
            await event.edit("**Xahiş olunur bir dil faylına cavab verin!**")
    elif search(r"məlumat|info", əmr):
        await event.edit("`Dil faylının məlumatları gətirilir... Xahiş olunur gözləyin.`")
        if event.is_reply:
            reply = await event.get_reply_message()
            if ((len(reply.file.name.split(".")) >= 1) and (not reply.file.name.split(".")[1] == "brendson")):
                return await event.edit("`Xahiş olunur düzgün` **BrendJSON** `faylı verin!`")

            fayl = await reply.download_media()

            try:
                fayl = loads(open(fayl, "r").read())
            except JSONDecodeError:
                return await event.edit("`Xahiş olunur düzgün` **BrendJSON** `faylı verin!`")

            await event.edit(
                f"**Dil: **`{fayl['LANGUAGE']}`\n"
                f"**Dil Kodu: **`{fayl['LANGCODE']}`\n"
                f"**Çevirən: **`{fayl['AUTHOR']}`\n"

                f"\n\n`Dil dosyasını yüklemek için` `.dil yükle` `komutunu kullanınız.`"
            )
        else:
            await event.edit("**Xahiş olunur bir dil faylına cavab verin!**")
    else:
        await event.edit(
            f"**Dil: **`{LANGUAGE_JSON['LANGUAGE']}`\n"
            f"**Dil Kodu: **`{LANGUAGE_JSON['LANGCODE']}`\n"
            f"**Çevirən: **`{LANGUAGE_JSON ['AUTHOR']}`\n"

            f"\n\nDigər dillər üçün @BrendDil kanalına baxa bilərsən."
        )

CmdHelp('dil').add_command(
    'dil', None, 'Yüklədiyiniz dil haqqında məlumat verər.'
).add_command(
    'dil məlumat', None, 'Yüklədiyiniz dil faylı haqqında məlumat verər.'
).add_command(
    'dil yüklə', None, 'Cavab verdiyiniz dili yükləyər.'
).add()
