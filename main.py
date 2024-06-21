import os
from aiogram import Bot, Dispatcher, executor, types
import pandas as pd

from keep_alive import keep_alive
keep_alive()

bot = Bot(token=os.environ.get('BOT_TOKEN'))
dp = Dispatcher(bot)

# Directly set the bot token
# token = '7374004152:AAE_THg9kxd_3FoKS-qEDZ9WyRB3w-IC-2s'
# bot = Bot(token=token)
# dp = Dispatcher(bot)

# In-memory storage for user IDs
user_ids = set()

# Define a handler for the /start command
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    msg_start = (f"Hi, {message.from_user.first_name}\n\n"
                 f"Welcome to \"Eco Bot\" ☘\n\n")
    await message.reply(msg_start)

# Define a handler for the /users command to send the list of user IDs
@dp.message_handler(commands=['users'])
async def send_user_ids(message: types.Message):
    if user_ids:
        users_list = "\n".join(str(user_id) for user_id in user_ids)
        await message.reply(f"Bot users:\n{users_list}")
    else:
        await message.reply("No users found.")

# Define a handler for the /export command to send an Excel file with user IDs
@dp.message_handler(commands=['export'])
async def export_user_ids(message: types.Message):
    if user_ids:
        df = pd.DataFrame(list(user_ids), columns=['User ID'])
        file_path = 'user_ids.xlsx'
        df.to_excel(file_path, index=False)

        with open(file_path, 'rb') as file:
            await message.reply_document(file)
        
        # Optionally, remove the file after sending it
        os.remove(file_path)
    else:
        await message.reply("No users found.")

# Define a handler to echo all received messages and add user IDs to the list
@dp.message_handler()
async def echo_message(message: types.Message):
    user_ids.add(message.from_user.id)
    await message.answer(message.text)

# Main entry point
if __name__ == '__main__':
    print("Running...")
    executor.start_polling(dp, skip_updates=True)
