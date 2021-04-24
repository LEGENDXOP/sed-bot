import Cerina.modules.sql.captcha_sql as sql
from Cerina import tbot, CMD_HELP
from Cerina.events import is_admin
from . import can_change_info, ck_admin
import os
from telethon import Button, events

turnon = ["on", "yes", "y"]
turnoff = ["off", "no", "n"]

async def extract_time(message, time_val):
    if any(time_val.endswith(unit) for unit in ("m", "h", "d")):
        unit = time_val[-1]
        time_num = time_val[:-1]
        if not time_num.isdigit():
            await message.reply(f"Invalid time type specified. Expected m,h, or d, got: {unit}")
            return False

        if unit == "m" or unit == "minute":
            bantime = int(time_num) * 60
        elif unit == "h" or unit == "hour":
            bantime = int(time_num) * 60 * 60
        elif unit == "d" or unit == "day":
            bantime = int(time_num) * 24 * 60 * 60
        else:
            return False
        return bantime
    else:
        await message.reply(
            "Invalid time type specified. Expected m,h, or d, got: {}".format(
                time_val[-1]
            )
        )
        return


@tbot.on(events.NewMessage(pattern="^[!?/]captcha ?(.*)"))
async def lel(event):
 args = event.pattern_match.group(1)
 avoid = ["kick", "mode on", "kicktime", "kick", "kick off", "kick yes", "kick on", "kick no", "kick y", "kick n", "mode off", "mode on", "mode y", "mode n", "mode yes", "mode no", "kicktime [0-9]d", "time", "time [0-9]"]
 if args:
  if args in avoid:
   return
 if event.is_private:
   return await event.reply("This command is made to be used in group chats, not in pm!")
 if not await ck_admin(event, event.sender_id):
   return await event.reply("Only admins can execute this command.")
 if not await can_change_info(message=event):
   return await event.reply("You are missing the following rights to use this command:CanChangeInfo!")
 settings = sql.get_mode(event.chat_id)
 if not args:
  if settings == True:
   await event.reply("Users will be asked to complete a CAPTCHA before being allowed to speak in the chat.\nTo change this setting, try this command again followed by one of yes/no/on/off")
  elif settings == False:
   await event.reply("Users will NOT be muted when joining the chat.\nTo change this setting, try this command again followed by one of yes/no/on/off")
 elif args in turnon:
  mode = True
  await event.reply("CAPTCHAs have been enabled. I will now mute people when they join.")
  x = sql.set_mode(event.chat_id, mode)
  if not x:
    sql.set_captcha(event.chat_id, "button")
 elif args in turnoff:
  mode = False
  await event.reply("CAPTCHAs have been disabled. Users can join normally.")
  x = sql.set_mode(event.chat_id, mode)

@tbot.on(events.NewMessage(pattern="^[!?/]captchatime ?(.*)"))
@is_admin
async def lel(event, perm):
 if not perm.change_info:
         await event.reply("You are missing the following rights to use this command:CanChangeInfo!")
         return
 settings = sql.get_unmute_time(event.chat_id)
 args = event.pattern_match.group(1)
 if not args:
  if settings == 0:
   await event.reply("Users will stay muted until they use the CAPTCHA.\nTo change the CAPTCHA mute time, try this command again with a time value.\nExample time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks.")
  elif settings > 0:
    tyme = settings/60
    unit = "Minutes"
    if tyme >= 60:
      tyme = tyme/60
      unit = "Hours"
    tt = f"{int(tyme)} {unit}"
    await event.reply(f"If users haven't unmuted themselves after {tt}, they will be unmuted automatically.\nTo change the CAPTCHA mute time, try this command again with a time value.\nExample time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks.")
 elif args in turnoff:
  mutetime = 0
  x = sql.set_unmute_time(event.chat_id, mutetime)
  await event.reply("I will now mute users for an indeterminate amount of time. The only way for them to get unmuted will be to complete the CAPTCHA.")
 elif args:
  mutetime = await extract_time(event, args)
  if mutetime:
   x = sql.set_unmute_time(event.chat_id, mutetime)
   await event.reply(f"I will now mute people for {args} when they join - or until they solve the CAPTCHA in the welcome message.")
  
@tbot.on(events.NewMessage(pattern="^[!?/]captchamode ?(.*)"))
@is_admin
async def lel(event, perm):
 options = ["math", "button", "text", "multibutton"]
 if not perm.change_info:
         await event.reply("You are missing the following rights to use this command:CanChangeInfo!")
         return
 settings = sql.get_style(event.chat_id)
 args = event.pattern_match.group(1)
 if not args:
  text = ""
  if settings == False:
   await event.reply("Enable CAPTCHAs First.!")
  elif settings in options:
   if settings == "button":
    text = """
The current CAPTCHA mode is: button
Button CAPTCHAs simply require a user to press a button in their welcome message to confirm they're human.

Available CAPTCHA modes are: button/math/text/multibutton
"""
   elif settings == "text":
    text = """
The current CAPTCHA mode is: text
Text CAPTCHAs require the user to answer a CAPTCHA containing letters and numbers.

Available CAPTCHA modes are: button/math/text/mutlibutton
"""
   elif settings == "math":
    text = """
The current CAPTCHA mode is: math
Math CAPTCHAs require the user to solve a basic maths question. Please note that this may discriminate against users with little maths knowledge.

Available CAPTCHA modes are: button/math/text/multibutton
"""
   elif settings == "multibutton":
    text = """
The current CAPTCHA mode is: multibutton
Multibutton CAPTCHAs require users to solve a button puzzle

Available CAPTCHA modes are: button/math/text/multibutton
"""
  await event.reply(text)
 elif args in options:
  style = args
  text = "CAPTCHAs set to **{}**.".format(style)
  await event.reply(text)
  x = sql.set_style(event.chat_id, style)
  if not x:
   sql.set_captcha(event.chat_id, style)
 else:
  await event.reply(f"{args} is not a recognised CAPTCHA mode! Try one of: button/math/text/multibutton")


@tbot.on(events.NewMessage(pattern="^[!?/]captchakick ?(.*)"))
async def lel(event):
 if event.is_private:
   return await event.reply("This command is made to be used in group chats, not in pm!")
 if not await ck_admin(event, event.sender_id):
   return await event.reply("Only admins can execute this command.")
 if not await can_change_info(message=event):
   return await event.reply("You are missing the following rights to use this command:CanChangeInfo!")
 optionsp = ["y", "yes", "on"]
 optionsn = ["n", "no", "off"]
 args= event.pattern_match.group(1)
 avoid = ["time", "time [0-9]", "time [0-9][hmd]"]
 if args:
  if args in avoid:
   return
 time = 300
 settings = sql.get_time(event.chat_id)
 if not args:
   if settings == False or settings == 0:
    await event.reply("""Users that don't complete their CAPTCHA are allowed to stay in the chat, muted, and can complete the CAPTCHA whenever.

To change this setting, try this command again followed by one of yes/no/on/off""")
   else:
    tyme = settings/60
    unit = "Minutes"
    if tyme >= 60:
      tyme = tyme/60
      unit = "Hours"
    tt = f"{int(tyme)} {unit}"
    await event.reply(f"""I am currently kicking users that haven't completed the CAPTCHA after {tt}

To change this setting, try this command again followed by one of yes/no/on/off""")
 elif args in optionsp:
  if settings:
   time = settings
  await event.reply(f"I will now kick people that haven't solved the CAPTCHA after {time/60} minutes.")
 elif args in optionsn:
  time = 0
  await event.reply("I will no longer kick people that haven't solved the CAPTCHA.")
 x = sql.set_time(event.chat_id, time)

@tbot.on(events.NewMessage(pattern="^[!?/]captchakicktime ?(.*)"))
@is_admin
async def lel(event, perm):
 if not perm.change_info:
         await event.reply("You are missing the following rights to use this command:CanChangeInfo!")
         return
 time = event.pattern_match.group(1)
 if time: mutetime = await extract_time(event, time)
 settings = sql.get_time(event.chat_id)
 if not time:
   if settings == False or settings == 0:
    await event.reply("Users that don't complete their CAPTCHA are allowed to stay in the chat, muted, and can complete the CAPTCHA whenever.To change this setting, try this command again followed by one of yes/no/on/off")
   else:
    tyme = settings/60
    unit = "Minutes"
    if tyme >= 60:
      tyme = tyme/60
      unit = "Hours"
    tt = f"{int(tyme)} {unit}"
    await event.reply(f"I am currently kicking users that haven't completed the CAPTCHA after {tt}")
 if mutetime:
  if mutetime >= 86400 or mutetime < 300:
    return await event.reply("The welcome kick time can only be between 5 minutes, and 1 day. Please choose another time.")
  x = sql.set_time(event.chat_id, mutetime)
  if not x:
   return await event.reply("Enable captcha first!.")
  await event.reply(f"Welcome kick time has been set to {time}.")
  
#Soon
