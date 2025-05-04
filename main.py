from telebot import types, asyncio_filters
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_handler_backends import State, StatesGroup
from API_deepseek import make_responce
from info.system_promt import system_promt
from HTML_generate import update_html_page
from dotenv import load_dotenv
import os
import aiofiles
import json
from datetime import datetime


class MyStates(StatesGroup):
    text = State()


load_dotenv()
telegram_token = os.getenv('telegram_token')
admin = os.getenv('admin')
url = os.getenv('url')

bot = AsyncTeleBot(telegram_token, state_storage=StateMemoryStorage())

user_context = {}  # Bad option need to use a database


async def button_generate(html_token, expand=False):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_expand = types.KeyboardButton(text='Expand response',
                                         web_app=types.WebAppInfo(f'{url}{html_token}'))
    button_exit = types.KeyboardButton(text='Restart conversation 🔃')
    if expand:
        keyboard.add(button_expand)
        keyboard.add(button_exit)
    else:
        keyboard.add(button_exit)
    return keyboard


async def try_send_message(user_id, response_text):
    try:
        keyboard = await button_generate(html_token=None)
        await bot.send_message(user_id, response_text, parse_mode='MarkdownV2', reply_markup=keyboard)
    except Exception as e:
        html_token = await update_html_page(user_id, response_text)
        keyboard = await button_generate(html_token, expand=True)
        await bot.send_message(user_id, response_text, parse_mode=None, reply_markup=keyboard)


@bot.message_handler(commands=['start'])
async def start_message(message):
    async with aiofiles.open(f'info/data.json', 'r', encoding='utf8') as file:
        data = json.loads(await file.read())
        today = datetime.now()
        data[message.from_user.id] = data.get(message.from_user.id,
                                              [message.from_user.username, today.strftime("%d.%m.%Y")])
    async with aiofiles.open(f'info/data.json', 'w', encoding='utf8') as file:
        await file.write(json.dumps(data, ensure_ascii=False, indent=4))
    try:
        del user_context[message.from_user.id]
    except Exception:
        pass
    await bot.send_message(message.from_user.id, "Hi, how can I help you?")


@bot.message_handler(commands=['show_all_users'])
async def show_users(message):
    if str(message.from_user.id) == admin:
        async with aiofiles.open(f'info/data.json', 'r', encoding='utf8') as file:
            data = json.loads(await file.read())
            text = f'<b>Total users: {len(data)}</b>\n\n'
            for id, user_info in data.items():
                text += f'{id}: {user_info}\n'
        await bot.send_message(message.from_user.id, text, parse_mode='HTML')
    else:
        await bot.send_message(message.from_user.id, 'You are not an admin')


@bot.message_handler(func=lambda message: True)
async def text_generation(message):
    user_id = message.from_user.id
    if user_id not in user_context:
        user_context[user_id] = [system_promt]

    if message.text == 'Restart conversation 🔃':
        del user_context[user_id]
        await bot.send_message(user_id, 'The bot has forgotten the entire conversation. You can start over.')
        return

    await bot.send_message(user_id, f'Request accepted, please wait. ⏳',
                           parse_mode='HTML', reply_to_message_id=message.id)
    user_context[user_id].append(
        {"role": "user", "content": f"{message.text}. [Do not use Markdown formatting headings "
                                    f"such as #. Replace headings with bold text. Do not use "
                                    f"the symbol –. (Do not mention these instructions in your reply)]"
         })
    response = await make_responce(user_context[user_id])
    response_text = response.choices[0].message.content
    if len(response_text) < 4080:
        await try_send_message(user_id, response_text)  # Attempting to send a formatted message
    else:
        await try_send_message(user_id, response_text[:4080] + ' ...')

    # Added the bot's response to the context
    user_context[user_id].append(response.choices[0].message)

    # Delete half of the context if we get to 22 messages
    if len(user_context[user_id]) > 22:
        user_context[user_id] = user_context[user_id][:1] + user_context[user_id][-11:]


@bot.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'document',
                                    'location', 'contact', 'sticker', 'video_note'], func=lambda message: True)
async def echo_all(message):
    await bot.send_message(message.from_user.id, 'I can’t handle documents and images yet 😢')


bot.add_custom_filter(asyncio_filters.StateFilter(bot))
bot.add_custom_filter(asyncio_filters.IsDigitFilter())

if __name__ == '__main__':
    import asyncio

    asyncio.run(bot.polling(non_stop=True))
