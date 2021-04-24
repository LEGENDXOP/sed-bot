import inspect
import time
import logging
import re
from pathlib import Path

from telethon import events
from telethon.tl import functions
from telethon.tl import types

from Cerina import CMD_LIST, LOAD_PLUG, tbot
import glob
import sys

def register(**args):
    pattern = args.get("pattern")
    r_pattern = r"^[/]"

    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern

    args["pattern"] = pattern.replace("^/", r_pattern, 1)
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    reg = re.compile("(.*)")

    if pattern is not None:
        try:
            cmd = re.search(reg, pattern)
            try:
                cmd = cmd.group(1).replace("$", "").replace("\\", "").replace("^", "")
            except BaseException:
                pass

            try:
                CMD_LIST[file_test].append(cmd)
            except BaseException:
                CMD_LIST.update({file_test: [cmd]})
        except BaseException:
            pass

    def decorator(func):
        async def wrapper(check):
            if check.edit_date:
                return
            if check.fwd_from:
                return
            if check.is_group or check.is_private:
                pass
            try:
                await func(check)
                try:
                    LOAD_PLUG[file_test].append(func)
                except Exception:
                    LOAD_PLUG.update({file_test: [func]})
            except BaseException:
                return
            else:
                pass

        tbot.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper

    return decorator

import functools

def is_admin(func):
    @functools.wraps(func)
    async def a_c(event):
        if event.is_private:
          k = await event.reply("This command is made to be used in group chats, not in pm!")
          return 
        is_admin = False
        if not event.is_private:
            try:
                _s = await event.client.get_permissions(event.chat_id, event.sender_id)
                if _s.is_admin:
                    is_admin = True
            except:
                is_admin = False
        if is_admin:
            await func(event, _s)
        else:
            await event.reply("Only Admins can execute this command!")
    return a_c

def load_module(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import importlib
        import Cerina.events

        path = Path(f"Cerina/modules/{shortname}.py")
        name = "Cerina.modules.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print("Successfully imported " + shortname)
    else:
        import importlib
        import Cerina.events

        path = Path(f"Cerina/modules/{shortname}.py")
        name = "Cerina.modules.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.register = register
        mod.tbot = tbot
        mod.logger = logging.getLogger(shortname)
        spec.loader.exec_module(mod)
        sys.modules["Cerina.modules." + shortname] = mod
        print("Successfully imported " + shortname)


path = "Cerina/modules/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        load_module(shortname.replace(".py", ""))
