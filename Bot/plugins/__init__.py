'''
RenameBot
© Mrvishal2k2
'''
from pyrogram import filters
from Bot.config import Config


def auth_filter(_, __, m):
    if not Config.AUTH_USERS:
        return True
    user_id = m.from_user.id if m.from_user else None
    return user_id in Config.AUTH_USERS


authorized = filters.create(auth_filter)
