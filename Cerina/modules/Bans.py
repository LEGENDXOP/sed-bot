from Cerina import tbot, OWNER_ID, BOT_ID
from Cerina.events import is_admin
from . import ck_admin, get_user
from telethon import events, Button
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
import time

async def extract_time(message, time_val):
    if any(time_val.endswith(unit) for unit in ("m", "h", "d")):
        unit = time_val[-1]
        time_num = time_val[:-1]
        if not time_num.isdigit():
            await message.reply(f"Invalid time type specified. Expected m,h, or d, got: {unit}")
            return ""

        if unit == "m" or unit == "minute":
            bantime = int(time.time() + int(time_num) * 60)
        elif unit == "h" or unit == "hour":
            bantime = int(time.time() + int(time_num) * 60 * 60)
        elif unit == "d" or unit == "day":
            bantime = int(time.time() + int(time_num) * 24 * 60 * 60)
        else:
            return
        return bantime
    else:
        await message.reply(
            "Invalid time type specified. Expected m,h, or d, got: {}".format(
                time_val[-1]
            )
        )
        return


@tbot.on(events.NewMessage(pattern="^[!?/]kick ?(.*)"))
@is_admin
async def kick(event, perm):
    if event.is_private:
        await event.reply("This cmd is made to be used in groups not PM")
        return
    if not perm.ban_users:
         await event.reply("You are missing the following rights to use this command:CanBanUsers!")
         return
    try:
     user, reason = await get_user(event)
    except:
      return
    if await ck_admin(event, user.id):
        return await event.reply("Yeah lets start banning admins!")
    if reason:
      reason = f"\n**Reason:** {reason}"
    else:
      reason = ""
    try:
     await tbot.kick_participant(event.chat_id, user.id)
     await event.reply(f"Succesfully Kicked [{user.first_name}](tg://user?id={user.id}) from {event.chat.title}{reason}")
    except:
     await event.reply("Seems like I don't have enough rights to do that.")

@tbot.on(events.NewMessage(pattern="^[!?/]kickme"))
async def kickme(event):

    if event.is_private:
        await event.reply("This cmd is made to be used in groups not PM")
        return

    check = await tbot.get_permissions(event.chat_id, event.sender_id)
    if check.is_admin:
        await event.reply("Sorry but I can't kick admins!")
        return

    await event.reply("Ok, as your wish")
    await tbot.kick_participant(event.chat_id, event.sender_id)

@tbot.on(events.NewMessage(pattern="^[!?/]ban ?(.*)"))
@is_admin
async def ban(event, perm):
    if event.is_private:
        await event.reply("This cmd is made to be used in groups not PM")
        return
    if not perm.ban_users:
        await event.reply("You are missing the following rights to use this command:CanBanUsers!")
        return
    try:
     user, reason = await get_user(event)
    except:
      return
    if await ck_admin(event, user.id):
        return await event.reply("Yeah lets start banning admins!")
    if reason:
      reason = f"\n**Reason:** {reason}"
    else:
      reason = ""
    try:
     await tbot(EditBannedRequest(event.chat_id, user.id, ChatBannedRights(until_date=None, view_messages=True)))
     await event.reply(f"Succesfully Banned [{user.first_name}](tg://user?id={user.id}) from {event.chat.title}{reason}")
    except:
     await event.reply("Seems like I don't have enough rights to do that.")

@tbot.on(events.NewMessage(pattern="^[!?/]unban ?(.*)"))
@is_admin
async def unban(event, perm):
    if event.is_private:
        await event.reply("This cmd is made to be used in groups not PM")
        return
    if not perm.ban_users:
        await event.reply("You are missing the following rights to use this command:CanBanUsers!")
        return
    try:
     user, reason = await get_user(event)
    except:
      return
    if await ck_admin(event, user.id):
        return await event.reply("Yeah lets start unbanning admins!")
    if reason:
      reason = f"\n**Reason:** {reason}"
    else:
      reason = ""
    try:
     await tbot(EditBannedRequest(event.chat_id, user.id, ChatBannedRights(until_date=None, view_messages=False)))
     await event.reply(f"Succesfully Unbanned [{user.first_name}](tg://user?id={user.id}) in {event.chat.title}{reason}")
    except:
     await event.reply("Seems like I don't have enough rights to do that.")

@tbot.on(events.NewMessage(pattern="^[!?/]skick ?(.*)"))
@is_admin
async def skick(event, perm):
    if not perm.ban_users:
         await event.reply("You are missing the following rights to use this command:CanBanUsers!")
         return
    try:
     user, reason = await get_user(event)
    except:
      return
    if await ck_admin(event, user.id):
        return await event.reply("Yeah lets start kicking admins!")
    if reason:
      reason = f"\n**Reason:** {reason}"
    else:
      reason = ""
    try:
     await event.delete()
     await tbot.kick_participant(event.chat_id, user.id)
     await event.reply(f"Succesfully Kicked [{user.first_name}](tg://user?id={user.id}) from {event.chat.title}{reason}")
    except:
     await event.reply("Seems like I don't have enough rights to do that.")

@tbot.on(events.NewMessage(pattern="^[!?/]dkick ?(.*)"))
@is_admin
async def dkick(event, perm):
    if not perm.ban_users:
         await event.reply("You are missing the following rights to use this command:CanBanUsers!")
         return
    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("Reply to someone to delete it and kick the user!")
        return
    try:
     user, reason = await get_user(event)
    except:
      return
    if await ck_admin(event, user.id):
        return await event.reply("Yeah lets start kicking admins!")
    if reason:
      reason = f"\n**Reason:** {reason}"
    else:
      reason = ""
    try:
     await reply_msg.delete()
     await tbot.kick_participant(event.chat_id, user.id)
     await event.reply(f"Succesfully Kicked [{user.first_name}](tg://user?id={user.id}) from {event.chat.title}{reason}")
    except:
     await event.reply("Seems like I don't have enough rights to do that.")

@tbot.on(events.NewMessage(pattern="^[!?/]dban ?(.*)"))
@is_admin
async def dban(event, perm):
    if not perm.ban_users:
         await event.reply("You are missing the following rights to use this command:CanBanUsers!")
         return
    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("Reply to someone to delete it and ban the user!")
        return
    try:
     user, reason = await get_user(event)
    except:
      return
    if await ck_admin(event, user.id):
        return await event.reply("Yeah lets start banning admins!")
    if reason:
      reason = f"\n**Reason:** {reason}"
    else:
      reason = ""
    await reply_msg.delete()
    try:
     await tbot(EditBannedRequest(event.chat_id, user.id, ChatBannedRights(until_date=None, view_messages=True)))
     await event.reply(f"Succesfully Banned [{user.first_name}](tg://user?id={user.id}) from {event.chat.title}{reason}")
    except:
     await event.reply("Seems like I don't have enough rights to do that.")

@tbot.on(events.NewMessage(pattern="^[!?/]sban ?(.*)"))
@is_admin
async def sban(event, perm):
    if not perm.ban_users:
         await event.reply("You are missing the following rights to use this command:CanBanUsers!")
         return
    try:
     user, reason = await get_user(event)
    except:
      return
    if await ck_admin(event, user.id):
        return await event.reply("Yeah lets start banning admins!")
    if reason:
      reason = f"\n**Reason:** {reason}"
    else:
      reason = ""
    await event.delete()
    try:
     await tbot(EditBannedRequest(event.chat_id, user.id, ChatBannedRights(until_date=None, view_messages=True)))
     await event.reply(f"Succesfully Banned [{user.first_name}](tg://user?id={user.id}) from {event.chat.title}{reason}")
    except:
     await event.reply("Seems like I don't have enough rights to do that.")


@tbot.on(events.NewMessage(pattern="^[!/?]tmute ?(.*)"))
@is_admin
async def tmute(event, perm):
 if event.is_private:
    return await event.reply("This command is made to be used in group chats, not in pm!")
 if not perm.ban_users:
         await event.reply("You are missing the following rights to use this command:CanBanUsers!")
         return
 try:
     user, reason = await get_user(event)
 except:
      return
 if await ck_admin(event, user.id):
        return await event.reply("Yeah lets start muting admins!")
 if not args:
   return await event.reply("You haven't specified a time to mute this user for!")
 input = args.split(" ", 1)
 if len(input) == 2:
   time = input[0]
   reason = input[1]
 elif len(input) == 1:
   time = input[0]
   reason = None
 if reason:
   reason = f"**Reason:** {reason}"
 else:
   reason = ""
 if len(time) == 1:
   return await event.reply(f"Invalid time type specified. Expected m,h, or d, got: {time}")
 mutetime = await extract_time(event, time)
 await tbot.edit_permissions(event.chat_id, user.id, send_messages=False, until_date=mutetime)
 replied_user = await tbot.get_entity(user.id)
 await event.respond(f'Muted **{replied_user.first_name}** for {args}!\n{reason}')

@tbot.on(events.NewMessage(pattern="^[!/?]tban ?(.*)"))
@is_admin
async def tmute(event, perm):
 if event.is_private:
    return await event.reply("This command is made to be used in group chats, not in pm!")
 if not perm.ban_users:
         await event.reply("You are missing the following rights to use this command:CanBanUsers!")
         return
 try:
     user, reason = await get_user(event)
 except:
      return
 if await ck_admin(event, user.id):
        return await event.reply("Yeah lets start banning admins!")
 if not args:
   return await event.reply("You haven't specified a time to ban this user for!")
 input = args.split(" ", 1)
 if len(input) == 2:
   time = input[0]
   reason = input[1]
 elif len(input) == 1:
   time = input[0]
   reason = None
 if reason:
   reason = f"**Reason:** {reason}"
 else:
   reason = ""
 if len(time) == 1:
   return await event.reply(f"Invalid time type specified. Expected m,h, or d, got: {time}")
 mutetime = await extract_time(event, time)
 await tbot.edit_permissions(event.chat_id, user.id, view_messages=False, until_date=mutetime)
 replied_user = await tbot.get_entity(user.id)
 await event.respond(f'Banned **{replied_user.first_name}** for {args}!\n{reason}')

@tbot.on(events.NewMessage(pattern="^[!/?]dmute ?(.*)"))
@is_admin
async def dban(event, perm):
  if event.is_private:
    return await event.reply("This command is made to be used in group chats, not in pm!")
  try:
     user, reason = await get_user(event)
  except:
      return
  if not perm.ban_users:
         await event.reply("You are missing the following rights to use this command:CanBanUsers!")
         return
  reply_msg = await event.get_reply_message()
  if not reply_msg:
        await event.reply("Reply to someone to delete it and mute the user!")
        return
  if await ck_admin(event, user.id):
        return await event.reply("Yeah lets start banning admins!")   
  if reason:
      reason = f"\n**Reason:** {reason}"
  else:
      reason = ""
  await reply_msg.delete()
  try:
   await tbot.edit_permissions(event.chat_id, user.id, send_messages=False)
   await event.reply(f"Shh.. quiet now.!\nMuted **{user.first_name}** {reason}")
  except:
   await event.reply("Seems like I don't have enough rights to do that.")

@tbot.on(events.NewMessage(pattern="^[!/?]mute ?(.*)"))
@is_admin
async def dban(event, perm):
  if event.is_private:
    return await event.reply("This command is made to be used in group chats, not in pm!")
  try:
     user, reason = await get_user(event)
  except:
      return
  if not perm.ban_users:
         await event.reply("You are missing the following rights to use this command:CanBanUsers!")
         return
  if await ck_admin(event, user.id):
        return await event.reply("Yeah lets start banning admins!")   
  if reason:
      reason = f"\n**Reason:** {reason}"
  else:
      reason = ""
  try:
   await tbot.edit_permissions(event.chat_id, user.id, send_messages=False)
   await event.reply(f"Shh.. quiet now.!\nMuted **{user.first_name}** {reason}")
  except:
   await event.reply("Seems like I don't have enough rights to do that.")

@tbot.on(events.NewMessage(pattern="^[!/?]smute ?(.*)"))
@is_admin
async def dban(event, perm):
  if event.is_private:
    return await event.reply("This command is made to be used in group chats, not in pm!")
  try:
     user, reason = await get_user(event)
  except:
      return
  if not perm.ban_users:
         await event.reply("You are missing the following rights to use this command:CanBanUsers!")
         return
  if await ck_admin(event, user.id):
        return await event.reply("Yeah lets start banning admins!")   
  if reason:
      reason = f"\n**Reason:** {reason}"
  else:
      reason = ""
  await event.delete()
  try:
   await tbot.edit_permissions(event.chat_id, user.id, send_messages=False)
   await event.reply(f"Shh.. quiet now.!\nMuted **{user.first_name}** {reason}")
  except:
   await event.reply("Seems like I don't have enough rights to do that.")

@tbot.on(events.callbackquery.CallbackQuery(data="bans"))
async def banhelp(event):
    await event.reply(help, buttons=[[Button.inline("« Bᴀᴄᴋ", data="help")]])

help = """
**User Commands:**
- /kickme: kicks the user

**Admin Commands:**
- /ban: Ban a user.
- /dban: Ban a user by reply, and delete their message.
- /sban: Silently ban a user, and delete your message.
- /tban: Temporarily ban a user.
- /unban: Unban a user.
- /mute: Mute a user.
- /dmute: Mute a user by reply, and delete their message.
- /smute: Silently mute a user, and delete your message.
- /tmute: Temporarily mute a user.
- /unmute: Unmute a user.
- /kick: Kick a user.
- /dkick: Kick a user by reply, and delete their message.
- /skick: Silently kick a user, and delete your message
"""
