import importlib
from importlib import import_module
from sqlite3 import connect
import os
import requests
from telethon.tl.types import InputMessagesFilterDocument
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from telethon.tl.functions.channels import GetMessagesRequest
from . import BRAIN_CHECKER, LOGS, bot, PLUGIN_CHANNEL_ID, CMD_HELP, LANGUAGE, BREND_VERSION, PATTERNS
from .modules import ALL_MODULES
import userbot.modules.sql_helper.mesaj_sql as MSJ_SQL
import userbot.modules.sql_helper.galeri_sql as GALERI_SQL
from pySmartDL import SmartDL
from telethon.tl import functions

from random import choice
import chromedriver_autoinstaller
from json import loads, JSONDecodeError
import re
import userbot.cmdhelp

DIZCILIK_STR = [
    "Stikeri fırladıram...",
    "Yaşasın fırlatmaq...",
    "Bu stikeri öz paketimə əlavə edirəm...",
    "Bunu fırlatmağım lazımdı...",
    "Hey bu nə gözəl bir stikerdi!\nBunu fırladıram..",
    "Stikeri fırladıram\nhahaha :).",
    "Hey buna bir bax. (☉｡☉)!→\nMən bunu fırladarkən...",
    "Güllər qırmızı göy üzü isə mavi, bu stikeri paketimə fırladaraq cool olacağam...",
    "Stiker oğurlanır..."
    "Bu stiker daha mənimdi... ",
]

AFKSTR = [
    "Hörmətli {mention} Hal-hazırda tələsirəm, sonra mesaj yazsan olmazmı? Onsuz da yenə gələcəm.",
    "Zəng etdiyiniz şəxs hazırda telefona cavab verə bilmir. Siqnal səsindən sonra mesajınızı göndərə bilərsiniz. Xidmət haqqı 20qəpik təşkil edir. \n`biiiiiiiiiiiiiiiiiiiiiiiiiiiiip`!",
    "Bir neçə dəqiqəyə qayıdacağam. Ancaq gəlməsəm ... daha çox gözlə.",
    "Mən indi burada deyiləm, yəqin ki, başqa bir yerdəyəm.",
    "Getsən gedirsənsə sevgili yar amma unutma nə vaxtsa geri dönəcəm.",
    "Bəzən həyatda ən yaxşı şeylər gözləməyə dəyər ... \ nHəqiqətən.",
    "Mən dərhal qayıdacağam, amma geri qayıtmasam, daha sonra qayıdacağam.",
    "Hələ başa düşmürsənsə, mən burada deyiləm.",
    "Salam, uzaq mesajıma xoş gəldiniz, bu gün sizi necə görməməzlikdən gələ bilərəm?",
    "7 dənizdən və 7 ölkədən, \ n7 su və 7 qitədən, \ n7 dağ və 7 təpədən, \ n7 düzənlik və 7 kurqandan, \ n7 hovuz və 7 göldən, \ n7 bahar və 7 çəmənlikdən, \ n7 şəhərdən və 7-dən uzağam. məhəllələr, \ n7 məhəllə və 7 ev ... \ n \ nMesajlarınızın belə mənə çatamayacağı yer!",
    "İndi klaviaturadan uzaqdayam, ama ekranınızda yeterincə yüksək səslə qışqırığ atsanız, sizi eşidə bilərəm.",
    "İnan bu dəqiqə burda olub sənlə yazışmağı çox istərdim ama işlərim var",
    "Bu tərəfdən irəlləyirəm\n<----",
    "Zəhmət olmasa mesaj buraxın və məni olduğumdan daha önəmli hiss etdirin.",
    "Sahibim burda deil, buna görə mənə yazmağı dayandır.",
    "Burda olsaydım,\nSənə harada olduğumu deyərdim.\n\nAma mən deiləm,\ngeri qayıtdığımda məndən soruş...",
    "Uzaqlardayam!\nNə vaxt qayıdaram bilmirəm !\nBəlkə bir neçə dəqiqə sonra!",
    "Sahibim indi məşğuldu. Adınızı, nömrənizi və adresinizi versəniz ona yönləndirərəm və beləliklə geri gəldiyi zaman, sizə cavab yazar",
    "Bağışlayın, sahibim burda deil.\nO gələnə qədər mənimlə danışa bilərsən.\nSahibim sizə sonra yazar.",
    "Dünən gecə yarə namə yazdım qalmışam əllərdə ayaqlarda denən heç halımı soruşmazmı? Qalmışam əllərdə ayaqlarda\nSahibim burda deil ama sənə mahnı oxuyajammmm",
    "Həyat qısa, dəyməz qıza...\nNətər zarafat elədim?",
    "İndi burada deiləm....\nama burda olsaydım...\n\nbu möhtəşəm olardı eləmi qadan alım ?",
]

UNAPPROVED_MSG = ("`Hey,`Salam {mention}`! Narahat olma mən bir botam.\n\n`"
                  "`Sahibim sənə PM(özəldən mesaj) atma icazəsi verməyib. `"
                  "`Xaiş edirəm sahibimin icazə verməsini gözləyin, mən ona tabeyəm.\n\n`"
                  "`Bildiyim qədəri ilə o gələn-gednənə PM icazəsi vermir.")

DB = connect("dtbbrain.check")
CURSOR = DB.cursor()
CURSOR.execute("""SELECT * FROM BRAIN1""")
ALL_ROWS = CURSOR.fetchall()
INVALID_PH = '\nHATA: Girilən telefon nömrəsi etibarsızdır' \
             '\n  Ipucu: Ölkə kodunuzu istifadə edərək nömrənizi daxil edin' \
             '\n       Telefon nömrənizi yenidən yoxlayın'

for i in ALL_ROWS:
    BRAIN_CHECKER.append(i[0])
connect("brendbrain").close()

def extractCommands(file):
    FileRead = open(file, 'r').read()

    if '/' in file:
        file = file.split('/')[-1]

    Pattern = re.findall(r"@register\(.*pattern=(r|)\"(.*)\".*\)", FileRead)
    Komutlar = []

    if re.search(r'CmdHelp\(.*\)', FileRead):
        pass
    else:
        dosyaAdi = file.replace('.py', '')
        CmdHelp = userbot.cmdhelp.CmdHelp(dosyaAdi, False)

        # Komutları Alırıq #
        for Command in Pattern:
            Command = Command[1]
            if Command == '' or len(Command) <= 1:
                continue
            Komut = re.findall("(^.*[a-zA-Z0-9şğüöçı]\w)", Command)
            if (len(Komut) >= 1) and (not Komut[0] == ''):
                Komut = Komut[0]
                if Komut[0] == '^':
                    KomutStr = Komut[1:]
                    if KomutStr[0] == '.':
                        KomutStr = KomutStr[1:]
                    Komutlar.append(KomutStr)
                else:
                    if Command[0] == '^':
                        KomutStr = Command[1:]
                        if KomutStr[0] == '.':
                            KomutStr = KomutStr[1:]
                        else:
                            KomutStr = Command
                        Komutlar.append(KomutStr)

            Brendpy = re.search('\"\"\"BRENDPY(.*)\"\"\"', FileRead, re.DOTALL)
            if not Brendpy == None:
                Brendpy = Brendpy.group(0)
                for Satir in Brendpy.splitlines():
                    if (not '"""' in Satir) and (':' in Satir):
                        Satir = Satir.split(':')
                        Isim = Satir[0]
                        Deger = Satir[1][1:]
                                
                        if Isim == 'INFO':
                            CmdHelp.add_info(Deger)
                        elif Isim == 'WARN':
                            CmdHelp.add_warning(Deger)
                        else:
                            CmdHelp.set_file_info(Isim, Deger)
            for Komut in Komutlar:
                CmdHelp.add_command(Komut, None, 'Bu plugin kənardann yüklənib. Hər-hansısa bir açıqlama müəyyən edilmədi.')
            CmdHelp.add()

try:
    bot.start()
    idim = bot.get_me().id
    DTBbl = requests.get('https://gitlab.com/valiant_userbot/brend-userbot/-/raw/master/brend.json').json()
    if idim in brendbl:
        bot.disconnect()

    try:
        chromedriver_autoinstaller.install()
    except:
        pass
    
    GALERI = {}
    PLUGIN_MESAJLAR = {}
    ORJ_PLUGIN_MESAJLAR = {"alive": "`Userbot {mention} üçün işləyir", "afk": f"`{str(choice(AFKSTR))}`", "kickme": "`Özünüzdən muğayat olun mən getdim `👋", "pm": UNAPPROVED_MSG, "dızcı": str(choice(DIZCILIK_STR)), "ban": "{mention}`, banlandı!`", "mute": "{mention}`, artıq səssizə alındı!`", "approve": "{mention}`, mənə mesaj göndərə bilərsən!`", "disapprove": "{mention}`, artıq mənə mesaj göndərə bilməzsən! '", "block": "{mention}`, bloklandın!`"}

    PLUGIN_MESAJLAR_TURLER = ["alive", "afk", "kickme", "pm", "dızcı", "ban", "mute", "approve", "disapprove", "block"]
    for mesaj in PLUGIN_MESAJLAR_TURLER:
        dmsj = MSJ_SQL.getir_mesaj(mesaj)
        if dmsj == False:
            PLUGIN_MESAJLAR[mesaj] = ORJ_PLUGIN_MESAJLAR[mesaj]
        else:
            if dmsj.startswith("MEDYA_"):
                medya = int(dmsj.split("MEDYA_")[1])
                medya = bot.get_messages(PLUGIN_CHANNEL_ID, ids=medya)

                PLUGIN_MESAJLAR[mesaj] = medya
            else:
                PLUGIN_MESAJLAR[mesaj] = dmsj
    if not PLUGIN_CHANNEL_ID == None:
        LOGS.info("Pluginlər Yüklənir")
        try:
            KanalId = bot.get_entity(PLUGIN_CHANNEL_ID)
        except:
            KanalId = "me"

        for plugin in bot.iter_messages(KanalId, filter=InputMessagesFilterDocument):
            if plugin.file.name and (len(plugin.file.name.split('.')) > 1) \
                and plugin.file.name.split('.')[-1] == 'py':
                Split = plugin.file.name.split('.')

                if not os.path.exists("./userbot/modules/" + plugin.file.name):
                    dosya = bot.download_media(plugin, "./userbot/modules/")
                else:
                    LOGS.info("Bu Plugin artıq quraşdırılıb! " + plugin.file.name)
                    extractCommands('./userbot/modules/' + plugin.file.name)
                    dosya = plugin.file.name
                    continue 
                
                try:
                    spec = importlib.util.spec_from_file_location("userbot.modules." + Split[0], dosya)
                    mod = importlib.util.module_from_spec(spec)

                    spec.loader.exec_module(mod)
                except Exception as e:
                    LOGS.info(f"`Yüklənmə uğursuzdur! Plugində xəta var.\n\nXəta: {e}`")

                    try:
                        plugin.delete()
                    except:
                        pass

                    if os.path.exists("./userbot/modules/" + plugin.file.name):
                        os.remove("./userbot/modules/" + plugin.file.name)
                    continue
                extractCommands('./userbot/modules/' + plugin.file.name)
    else:
        bot.send_message("me", f"`Xaiş edirəm, pluginlərin qalıcı olması üçün . PLUGIN_CHANNEL_ID'i quraşdırın.`")
except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

async def FotoDegistir (foto):
    FOTOURL = GALERI_SQL.TUM_GALERI[foto].foto
    r = requests.get(FOTOURL)

    with open(str(foto) + ".jpg", 'wb') as f:
        f.write(r.content)    
    file = await bot.upload_file(str(foto) + ".jpg")
    try:
        await bot(functions.photos.UploadProfilePhotoRequest(
            file
        ))
        return True
    except:
        return False

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info("Botunuz hazırdır və işləyir! Hər-hansısa bir söhbətdə .alive yazaraq yoxlaya bilərsiniz."
          " Köməyə ehtiyacınız olarsa, Dəstək qrupumuza gəlin t.me/BrendSupport")
LOGS.info(f"Bot versiyanız:  {BREND_VERSION}")

"""
if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
"""
bot.run_until_disconnected()
