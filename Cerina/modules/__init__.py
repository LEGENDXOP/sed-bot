from Cerina import tbot, MONGO_DB_URI
from telethon import functions, types
from pymongo import MongoClient
import random
import Cerina.modules.sql.elevated_sql as sql
from captcha.image import ImageCaptcha

#Setup SUDO
SUDO_USERS = []
Elevated = sql.SUDO_USERS
for x in Elevated:
    SUDO_USERS.append(x)

#mongodb
client = MongoClient(MONGO_DB_URI)
db = client["Cerina"]

async def get_user(event):
    args = event.pattern_match.group(1).split(" ", 1)
    extra = ""
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.reply("I don't know who you're talking about, you're going to need to specify a user...!")
            return
        try:
            user_obj = await tbot.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.reply(str(err))
            return

    return user_obj, extra

async def can_promote_users(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.add_admins
    )

async def can_change_info(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.change_info
    )

async def ck_admin(event, user):
    try:
        sed = await event.client.get_permissions(event.chat_id, user)
        if sed.is_admin:
            is_mod = True
        else:
            is_mod = False
    except:
        is_mod = False
    return is_mod

number_list = ['0','1','2','3','4','5','6','7','8','9']
alphabet_lowercase = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
alphabet_uppercase = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def gen_captcha(captcha_string_size=10):
    captcha_string_list = []
    base_char = alphabet_lowercase + alphabet_uppercase + number_list
    for i in range(captcha_string_size):
        char = random.choice(base_char)
        captcha_string_list.append(char)
    captcha_string = '' 
    for item in captcha_string_list:
        captcha_string += str(item)
    return captcha_string

def gen_img_captcha(captcha_string_size=10):
 image_captcha = ImageCaptcha(width = 400, height = 270)
 text = get_captcha(captcha_string_size)
 image_file = "./"+ "captcha.png"
 image_captcha.write(text, image_file)
 
