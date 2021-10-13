from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions import UserNotParticipant
from config import Config
from helpers import cartonize
import os

app = Client(
    "Cartonizer",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)


def joined():

    def decorator(func):

        async def wrapped(client, message : Message):

            try:
                check = await app.get_chat_member("SJ_Bots", message.from_user.id)
                if check.status in ['member','administrator','creator']:
                    await func(client, message)
                else:
                    await message.reply("💡 You must join our channel in order to use this bot.\n/start the bot again after joining",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("JOIN CHANNEL", url="https://t.me/SJ_Bots")]]))
            except UserNotParticipant as e:
                await message.reply("💡 You must join our channel in order to use this bot.\n/start the bot again after joining",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("JOIN CHANNEL", url="https://t.me/SJ_Bots")]]))

        return wrapped

    return decorator



@app.on_message(filters.command('start'))
@joined()
async def start(client, message : Message):
    await message.reply(f"**Hello**, @{message.from_user.username}\n"
                        "➖➖➖➖➖➖➖➖➖➖➖➖\n"
                        "**Send Any Of Your Image And I will Convert It Into A Cartoon**\n"
                        "➖➖➖➖➖➖➖➖➖➖➖➖\n"
                        "✅𝗖𝗥𝗘𝗗𝗜𝗧𝗦:- @SJ_Bots")


@app.on_message(filters.photo | filters.document)
@joined()
async def cartonize_lis(client, message : Message):
    msg = await message.reply("Processing...")
    img = await message.download()
    rel_img = os.path.relpath(img)
    cartoon = cartonize(rel_img)
    await message.reply_document(cartoon, 
                                caption="Here Is Your Cartoonized Image\n✅𝗖𝗥𝗘𝗗𝗜𝗧𝗦:- @SJCartonizer_bot\n© [SJ Bots](https://t.me/SJ_Bots)")
    await msg.delete()
    os.remove(cartoon)
    os.remove(rel_img)




app.run()