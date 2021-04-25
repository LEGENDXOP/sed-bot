from Cerina import tbot, OWNER_ID, BOT_ID
import Cerina.modules.sql.elevated_sql as sql
from Cerina.events import register
from . import get_user,SUDO_USERS
import subprocess, io, sys, os, asyncio, traceback
from telethon import events


@tbot.on(events.NewMessage(pattern="^[!/?.]addsudo ?(.*)"))
async def ss(event):
 if not event.sender_id == OWNER_ID:
   return
 user, arg = await get_user(event)
 user_id = user.id
 try:
   name = await tbot.get_entity(user.id)
   fname = name.first_name
 except:
   fname = "User"
 if user_id == OWNER_ID or user_id == BOT_ID:
   return
 if sql.is_sudo(user_id):
      await event.reply("This is already a Pro Sudo!")
      return
 await event.reply(f"Sucessfully set the Disaster level of this user to **Sudo User**.")
 sql.set_sudo(user_id, fname)
 SUDO_USERS.append(user_id)

@tbot.on(events.NewMessage(pattern="^[!/?.]remsudo ?(.*)"))
async def ss(event):
 if not event.sender_id == OWNER_ID:
   return
 user, arg = await get_user(event)
 user_id = user.id
 try:
   name = await tbot.get_entity(user.id)
   fname = name.first_name
 except:
   fname = "User"
 if user_id == OWNER_ID or user_id == BOT_ID:
   return
 if sql.is_sudo(user_id):
         sql.rm_sudo(user_id)
         await event.reply(f"Removed From **Sudo Users**.")
         SUDO_USERS.remove(user_id)
         return
 await event.reply("This is not event a Sudo User;(")
   

@tbot.on(events.NewMessage(pattern="^[!/?.]eval ?(.*)"))
async def _(event):
    cmd = event.text.split(" ", maxsplit=1)[1]
    if event.sender_id == OWNER_ID:
       pass
    else:
      return
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, event)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = "`{}`".format(evaluation)
    MAX_MESSAGE_SIZE_LIMIT = 4095
    if len(final_output) > MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await tbot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id,
            )

    else:
        await event.reply(final_output)

async def aexec(code, smessatatus):
    message = event = smessatatus

    def p(_x):
        return print(slitu.yaml_format(_x))

    reply = await event.get_reply_message()
    exec(
        "async def __aexec(message, reply, client, p): "
        + "\n event = smessatatus = message"
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](message, reply, tbot, p)
