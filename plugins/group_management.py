from pyrogram import Client, filters, enums
from utils import is_check_admin
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command('manage') & filters.group)
async def members_management(client, message):
  if not await is_check_admin(client, message.chat.id, message.from_user.id):
    return await message.reply_text('You not admin in this group.')
  btn = [[
    InlineKeyboardButton('Unmute All', callback_data=f'unmute_all_members'),
    InlineKeyboardButton('Unban All', callback_data=f'unban_all_members')
  ],[
    InlineKeyboardButton('Kick Muted Users', callback_data=f'kick_muted_members'),
    InlineKeyboardButton('Kick Deleted Accounts', callback_data=f'kick_deleted_accounts_members')
  ]]
  await message.reply_text("Select one of function to manage members.", reply_markup=InlineKeyboardMarkup(btn))

@Client.on_message(filters.command('promote') & filters.group)
async def add_group_admin(client, message):
    if not await is_check_admin(client, message.chat.id, message.from_user.id):
        return await message.reply_text('You are not an admin in this group.')

    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id
    else:
        try:
            user_id = message.text.split(" ", 1)[1]
        except IndexError:
            return await message.reply_text("Reply to any user message or provide the user id or username.")

    try:
        user_id = int(user_id)
    except ValueError:
        pass

    try:
        user = (await client.get_chat_member(message.chat.id, user_id)).user
    except:
        return await message.reply_text("Can't find the given user in this group.")
    permissions = ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_change_info=True,
        can_invite_users=True,
        can_pin_messages=True,
        )

    
    try:
        await client.promote_chat_member(message.chat.id, user_id,permissions=permissions)
    except:
        return await message.reply_text("I don't have access to add admin.")

    await message.reply_text(f'Successfully added {user.mention} as admin to {message.chat.title}')

  
@Client.on_message(filters.command('ban') & filters.group)
async def ban_chat_user(client, message):
  if not await is_check_admin(client, message.chat.id, message.from_user.id):
    return await message.reply_text('You not admin in this group.')
  if message.reply_to_message and message.reply_to_message.from_user:
    user_id = message.reply_to_message.from_user.username or message.reply_to_message.from_user.id
  else:
    try:
      user_id = message.text.split(" ", 1)[1]
    except IndexError:
      return await message.reply_text("Reply to any user message or give user id, username")
  try:
    user_id = int(user_id)
  except ValueError:
    pass
  try:
    user = (await client.get_chat_member(message.chat.id, user_id)).user
  except:
    return await message.reply_text("Can't find you given user in this group")
  try:
    await client.ban_chat_member(message.from_user.id, user_id)
  except:
    return await message.reply_text("I don't have access to ban user")
  await message.reply_text(f'Successfully banned {user.mention} from {message.chat.title}')


@Client.on_message(filters.command('mute') & filters.group)
async def mute_chat_user(client, message):
  if not await is_check_admin(client, message.chat.id, message.from_user.id):
    return await message.reply_text('You not admin in this group.')
  if message.reply_to_message and message.reply_to_message.from_user:
    user_id = message.reply_to_message.from_user.username or message.reply_to_message.from_user.id
  else:
    try:
      user_id = message.text.split(" ", 1)[1]
    except IndexError:
      return await message.reply_text("Reply to any user message or give user id, username")
  try:
    user_id = int(user_id)
  except ValueError:
    pass
  try:
    user = (await client.get_chat_member(message.chat.id, user_id)).user
  except:
    return await message.reply_text("Can't find you given user in this group")
  try:
    await client.restrict_chat_member(message.chat.id, user_id, ChatPermissions())
  except:
    return await message.reply_text("I don't have access to mute user")
  await message.reply_text(f'Successfully muted {user.mention} from {message.chat.title}')


@Client.on_message(filters.command(["unban", "unmute"]) & filters.group)
async def unban_chat_user(client, message):
  if not await is_check_admin(client, message.chat.id, message.from_user.id):
    return await message.reply_text('You not admin in this group.')
  if message.reply_to_message and message.reply_to_message.from_user:
    user_id = message.reply_to_message.from_user.username or message.reply_to_message.from_user.id
  else:
    try:
      user_id = message.text.split(" ", 1)[1]
    except IndexError:
      return await message.reply_text("Reply to any user message or give user id, username")
  try:
    user_id = int(user_id)
  except ValueError:
    pass
  try:
    user = (await client.get_chat_member(message.chat.id, user_id)).user
  except:
    return await message.reply_text("Can't find you given user in this group")
  try:
    await client.unban_chat_member(message.chat.id, user_id)
  except:
    return await message.reply_text(f"I don't have access to {message.command[0]} user")
  await message.reply_text(f'Successfully {message.command[0]} {user.mention} from {message.chat.title}')
