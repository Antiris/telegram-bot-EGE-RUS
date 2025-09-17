from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import itertools

import logging
import sqlite3
import datetime

import keyboards as key
import config
import bot_text
import command_info
import algorithm_rus
import rus_num_keyboards
import rus_otv_keyboards

storage = MemoryStorage()
logging.basicConfig(level = logging.INFO)
bot = Bot(token = config.bot_token, parse_mode = types.ParseMode.HTML)
dp = Dispatcher(bot, storage = storage)
db = sqlite3.connect(config.sqlite_base)
cursor = db.cursor()

class Otvet_rus(StatesGroup):
    otv_rus_4 = State()
    otv_rus_5 = State()
    otv_rus_6 = State()
    otv_rus_7 = State()
    otv_rus_8 = State()
    otv_rus_15 = State()

def check_sub_channel(chat_member):
    if chat_member['status'] != 'left':
        return True
    else:
        return False

@dp.message_handler(commands = ['start'])
async def start(message: types.Message):
    if message.chat.type == 'private':
        if check_sub_channel(await bot.get_chat_member(config.channelID, message.from_user.id)):
            info = cursor.execute('SELECT * FROM users_bot WHERE id=?', (message.from_user.id,))
            if info.fetchone() is None: 
                await bot.send_message(message.from_user.id, bot_text.start, reply_markup = key.sogl_pan)
            else: 
                await bot.send_message(message.from_user.id, bot_text.main, reply_markup = key.sc_pan)
        else:
            await bot.send_message(message.from_user.id, bot_text.No_sub, reply_markup=key.sub)

@dp.message_handler(commands = ['send'])
async def send(message: types.Message):
    if message.from_user.id in config.admin_id and message.chat.type == 'private':
        await bot.send_message(message.from_user.id, f'<b>📣 Рассылка началась...</b>')
        date = datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')
        k = s = u = 0
        r = cursor.execute('SELECT id FROM users_bot').fetchall()
        users = [r[i][0] for i in range(len(r))]
        for user in users:
            try:
                await bot.send_message(user, f'Рассылка!\n\n{message.text[6:]}', reply_markup = key.rulesdelete)
                k += 1
            except: s += 1
            u += 1
        await bot.send_message(message.from_user.id, f'<b>📣 Рассылка была успешна произведена!</b>\n\n<b>Отправитель:</b> @{message.from_user.username}\n<b>Время:</b> {date}\n<b>Текст:</b> {message.text[6:]}\n\n<b>✅ Получили:</b> {k}\n<b>🚫 Не получили:</b> {s}\n<b>👥 Всего пользователей:</b> {u}')

@dp.message_handler(commands = ['stats'])
async def stats(message: types.Message):
    if message.from_user.id in config.admin_id and message.chat.type == 'private':
        r = cursor.execute('SELECT id FROM users_bot').fetchall()
        users = len([r[i][0] for i in range(len(r))])
        await bot.send_message(message.from_user.id, f'Количество пользователей в боте: {users}')

@dp.message_handler(commands = ['donate'])
async def donate(message: types.Message): await bot.send_message(message.from_user.id, bot_text.donatelink)        

@dp.message_handler(commands = ['help'])
async def donate(message: types.Message): 
    if message.from_user.id in config.admin_id and message.chat.type == 'private':
        await bot.send_message(message.from_user.id, 'Список команд.\n\n/stats - Кол-во пользователей.\n/version - Версия проекта.\n/info - Статистика.', reply_markup = key.rulesdelete)
    else:    
        await bot.send_message(message.from_user.id, 'Нашли ошибку, то пишите @Elanimus', reply_markup = key.rulesdelete)   

@dp.message_handler(commands = ['version'])
async def version(message: types.Message): await bot.send_message(message.from_user.id, config.bot_version, reply_markup = key.rulesdelete)

@dp.message_handler(commands = ['info'])
async def statistics(message: types.Message):
    text = command_info.stats(message.from_user.id)
    await bot.send_message(message.from_user.id, text, reply_markup = key.rulesdelete)

# ------ ЗАПИСЬ ОТВЕТА ------
# 4 РУС
@dp.message_handler(state = Otvet_rus.otv_rus_4)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(otvet = message.text)
    data = await state.get_data()
    i = cursor.execute(f'SELECT * FROM users_bot WHERE id = ?', (message.from_user.id,)).fetchall()[0]
    k = cursor.execute(f'SELECT * FROM otvet_users WHERE id = ?', (message.from_user.id,)).fetchall()[0]
    cursor.execute(f'UPDATE users_bot SET count_rus = {i[2] + 1} WHERE id = {message.from_user.id}')
    cursor.execute(f'UPDATE users_bot SET count_rus4 = {i[4] + 1} WHERE id = {message.from_user.id}')
    cursor.execute(f"UPDATE date_users SET active = '{datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")}' WHERE id = {message.from_user.id}")
    await bot.delete_message(message.from_user.id, message_id = message.message_id - 1)
    await bot.delete_message(message.from_user.id, message_id = message.message_id)
    if data['otvet'] in [''.join(j) for j in itertools.permutations(str(k[1]))]:
        st = 'Верно'
        cursor.execute(f'UPDATE users_bot SET true_rus = {i[3] + 1} WHERE id = {message.from_user.id}')
        cursor.execute(f'UPDATE users_bot SET true_rus4 = {i[5] + 1} WHERE id = {message.from_user.id}')
    else: st = 'Неверно'
    db.commit()
    await message.answer(f"Ваш ответ: {data['otvet']}\n\nПравильный ответ: {k[1]} или любая другая последовательность этих цифр.\n\nПояснение.\nРасставим ударения:\n{k[2]}\nСтатус: {st}.", reply_markup = rus_otv_keyboards.rus_4_dal_pan)
    await state.finish()

# 5 РУС 
@dp.message_handler(state = Otvet_rus.otv_rus_5)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(otvet = message.text)
    data = await state.get_data()
    i = cursor.execute(f'SELECT * FROM users_bot WHERE id = ?', (message.from_user.id,)).fetchall()[0]
    k = cursor.execute(f'SELECT * FROM otvet_users WHERE id = ?', (message.from_user.id,)).fetchall()[0]
    cursor.execute(f'UPDATE users_bot SET count_rus = {i[2] + 1} WHERE id = {message.from_user.id}')
    cursor.execute(f'UPDATE users_bot SET count_rus5 = {i[6] + 1} WHERE id = {message.from_user.id}')
    cursor.execute(f'UPDATE date_users SET active = "{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')}" WHERE id = {message.from_user.id}')
    await bot.delete_message(message.from_user.id, message_id = message.message_id - 1)
    await bot.delete_message(message.from_user.id, message_id = message.message_id)
    if data['otvet'].lower() == k[1]:
        st = 'Верно'
        cursor.execute(f'UPDATE users_bot SET true_rus = {i[3] + 1} WHERE id = {message.from_user.id}')
        cursor.execute(f'UPDATE users_bot SET true_rus5 = {i[7] + 1} WHERE id = {message.from_user.id}')
    else: st = 'Неверно'
    db.commit()
    await message.answer(f"Ваш ответ: {data['otvet'].lower()}\n\nПравильный ответ: {k[1]}\n\nСтатус: {st}.", reply_markup = rus_otv_keyboards.rus_5_dal_pan)
    await state.finish()

# 6 РУС 
@dp.message_handler(state = Otvet_rus.otv_rus_6)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(otvet = message.text)
    data = await state.get_data()
    i = cursor.execute(f'SELECT * FROM users_bot WHERE id = ?', (message.from_user.id,)).fetchall()[0]
    k = cursor.execute(f'SELECT * FROM otvet_users WHERE id = ?', (message.from_user.id,)).fetchall()[0]
    cursor.execute(f'UPDATE users_bot SET count_rus = {i[2] + 1} WHERE id = {message.from_user.id}')
    cursor.execute(f'UPDATE users_bot SET count_rus6 = {i[8] + 1} WHERE id = {message.from_user.id}')
    cursor.execute(f'UPDATE date_users SET active = "{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')}" WHERE id = {message.from_user.id}')
    await bot.delete_message(message.from_user.id, message_id = message.message_id - 1)
    await bot.delete_message(message.from_user.id, message_id = message.message_id)
    if data['otvet'].lower() in k[1].split(' [или] '): 
        st = 'Верно'
        cursor.execute(f'UPDATE users_bot SET true_rus = {i[3] + 1} WHERE id = {message.from_user.id}')
        cursor.execute(f'UPDATE users_bot SET true_rus6 = {i[9] + 1} WHERE id = {message.from_user.id}')
    else: st = 'Неверно'
    db.commit()
    await message.answer(f"Ваш ответ: {data['otvet'].lower()}\n\nПравильный ответ: {k[1]}\n\nПояснение.\n{k[2]}\n\nСтатус: {st}.", reply_markup = rus_otv_keyboards.rus_6_dal_pan)
    await state.finish()

# 7 РУС 
@dp.message_handler(state = Otvet_rus.otv_rus_7)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(otvet = message.text)
    data = await state.get_data()
    i = cursor.execute(f'SELECT * FROM users_bot WHERE id = ?', (message.from_user.id,)).fetchall()[0]
    k = cursor.execute(f'SELECT * FROM otvet_users WHERE id = ?', (message.from_user.id,)).fetchall()[0]
    cursor.execute(f'UPDATE users_bot SET count_rus = {i[2] + 1} WHERE id = {message.from_user.id}')
    cursor.execute(f'UPDATE users_bot SET count_rus7 = {i[10] + 1} WHERE id = {message.from_user.id}')
    cursor.execute(f'UPDATE date_users SET active = "{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')}" WHERE id = {message.from_user.id}')
    await bot.delete_message(message.from_user.id, message_id = message.message_id - 1)
    await bot.delete_message(message.from_user.id, message_id = message.message_id)
    if data['otvet'].lower() in k[1].split(' [или] '):
        st = 'Верно'
        cursor.execute(f'UPDATE users_bot SET true_rus = {i[3] + 1} WHERE id = {message.from_user.id}')
        cursor.execute(f'UPDATE users_bot SET true_rus7 = {i[11] + 1} WHERE id = {message.from_user.id}')
    else: st = 'Неверно'
    db.commit()
    await message.answer(f"Ваш ответ: {data['otvet'].lower()}\n\nПравильный ответ: {k[1]}\n\nСтатус: {st}.", reply_markup = rus_otv_keyboards.rus_7_dal_pan)
    await state.finish()

# 8 РУС 
@dp.message_handler(state = Otvet_rus.otv_rus_8)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(otvet = message.text)
    data = await state.get_data()
    i = cursor.execute(f'SELECT * FROM users_bot WHERE id = ?', (message.from_user.id,)).fetchall()[0]
    k = cursor.execute(f'SELECT * FROM otvet_users WHERE id = ?', (message.from_user.id,)).fetchall()[0]
    cursor.execute(f'UPDATE users_bot SET count_rus = {i[2] + 1} WHERE id = {message.from_user.id}')
    cursor.execute(f'UPDATE users_bot SET count_rus8 = {i[12] + 1} WHERE id = {message.from_user.id}')
    a = list(data['otvet'])
    b = list(k[1])
    c = [a[i] == b[i] for i in range(5)].count(True)
    if c != 0:
        cursor.execute(f'UPDATE users_bot SET true_rus = {i[3] + 1} WHERE id = {message.from_user.id}')
    if c == 5:
        cursor.execute(f'UPDATE users_bot SET ball3_rus8 = {i[15] + 1} WHERE id = {message.from_user.id}')
    elif 3 <= c <= 4:
        cursor.execute(f'UPDATE users_bot SET ball2_rus8 = {i[14] + 1} WHERE id = {message.from_user.id}')
    elif 1 <= c <= 2:
        cursor.execute(f'UPDATE users_bot SET ball1_rus8 = {i[13] + 1} WHERE id = {message.from_user.id}')
    await message.answer(f"Ваш ответ: {data['otvet']}\n\nПравильный ответ: {k[1]}", reply_markup = rus_otv_keyboards.rus_8_dal_pan)
    db.commit()
    await state.finish()

# 15 РУС
@dp.message_handler(state = Otvet_rus.otv_rus_15)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(otvet = message.text)
    data = await state.get_data()
    i = cursor.execute(f'SELECT * FROM users_bot WHERE id = ?', (message.from_user.id,)).fetchall()[0]
    k = cursor.execute(f'SELECT * FROM otvet_users WHERE id = ?', (message.from_user.id,)).fetchall()[0]
    cursor.execute(f'UPDATE users_bot SET count_rus = {i[4] + 1} WHERE id = {message.from_user.id}')
    cursor.execute(f'UPDATE users_bot SET count_rus15 = {i[22] + 1} WHERE id = {message.from_user.id}')
    cursor.execute(f'UPDATE date_users SET active = "{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')}" WHERE id = {message.from_user.id}')
    await bot.delete_message(message.from_user.id, message_id = message.message_id - 1)
    await bot.delete_message(message.from_user.id, message_id = message.message_id)
    if data['otvet'] in [''.join(j) for j in itertools.permutations(str(k[1]))]:
        st = 'Верно'
        cursor.execute(f'UPDATE users_bot SET true_rus = {i[5] + 1} WHERE id = {message.from_user.id}')
        cursor.execute(f'UPDATE users_bot SET true_rus15 = {i[23] + 1} WHERE id = {message.from_user.id}')
    else: st = 'Неверно'
    await message.answer(f"Ваш ответ: {data['otvet']}\n\nПравильный ответ: {k[1]} или любая другая последовательность этих цифр.\n\nСтатус: {st}.", reply_markup = rus_otv_keyboards.rus_15_dal_pan)
    await state.finish()
    db.commit()

# РУССКИЙ
@dp.callback_query_handler(text = 'rus_types')
async def rus_types(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = bot_text.rus, reply_markup = rus_num_keyboards.rus_pan)

# ---------- КНОПКА ОТВЕТА ----------
# 4 РУС
@dp.callback_query_handler(text = 'otv_rus_4')
async def otv_rus_4(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, 'Введите ответ')
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = call.message.text)
    await Otvet_rus.otv_rus_4.set()

# 5 РУС
@dp.callback_query_handler(text = 'otv_rus_5')
async def otv_rus_5(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, 'Введите ответ')
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = call.message.text)
    await Otvet_rus.otv_rus_5.set()

# 6 РУС
@dp.callback_query_handler(text = 'otv_rus_6')
async def otv_rus_6(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, 'Введите ответ')
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = call.message.text)
    await Otvet_rus.otv_rus_6.set()

# 7 РУС
@dp.callback_query_handler(text = 'otv_rus_7')
async def otv_rus_7(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, 'Введите ответ')
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = call.message.text)
    await Otvet_rus.otv_rus_7.set()

# 8 РУС
@dp.callback_query_handler(text = 'otv_rus_8')
async def otv_rus_8(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, 'Введите ответ')
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = call.message.text)
    await Otvet_rus.otv_rus_8.set()


# 15 РУС
@dp.callback_query_handler(text = 'otv_rus_15')
async def otv_rus_15(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, 'Введите ответ')
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = call.message.text)
    await Otvet_rus.otv_rus_15.set()

# -------------- РУС 4
@dp.callback_query_handler(text = 'rus_4')
async def rus_4(call: types.CallbackQuery):
    text = algorithm_rus.rus_4(call.from_user.id)
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = call.message.text)
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = text, reply_markup = rus_otv_keyboards.rus_4_pan)
    
@dp.callback_query_handler(text = 'rus_4_1')
async def rus_4_1(call: types.CallbackQuery):
    text = algorithm_rus.rus_4(call.from_user.id)
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = call.message.text)
    await bot.send_message(call.from_user.id, text, reply_markup = rus_otv_keyboards.rus_4_pan)
    
# -------------- РУС 5
@dp.callback_query_handler(text = 'rus_5')
async def rus_5(call: types.CallbackQuery):
    text = algorithm_rus.rus_5(call.from_user.id)
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = call.message.text)
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = text, reply_markup = rus_otv_keyboards.rus_5_pan)
    db.commit()

@dp.callback_query_handler(text = 'rus_5_1')
async def rus_5_1(call: types.CallbackQuery):
    text = algorithm_rus.rus_5(call.from_user.id)
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = call.message.text)
    await bot.send_message(call.from_user.id, text, reply_markup = rus_otv_keyboards.rus_5_pan)
    
# -------------- РУС 6
@dp.callback_query_handler(text = 'rus_6')
async def rus_6(call: types.CallbackQuery):
    text = algorithm_rus.rus_6(call.from_user.id)
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = call.message.text)
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = text, reply_markup = rus_otv_keyboards.rus_6_pan)

@dp.callback_query_handler(text = 'rus_6_1')
async def rus_6_1(call: types.CallbackQuery):
    text = algorithm_rus.rus_6(call.from_user.id)
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = call.message.text)
    await bot.send_message(call.from_user.id, text, reply_markup = rus_otv_keyboards.rus_6_pan)

# -------------- РУС 7
@dp.callback_query_handler(text = 'rus_7')
async def rus_7(call: types.CallbackQuery):
    text = algorithm_rus.rus_7(call.from_user.id)
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = call.message.text)
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = text, reply_markup = rus_otv_keyboards.rus_7_pan)
    db.commit()

@dp.callback_query_handler(text = 'rus_7_1')
async def rus_7_1(call: types.CallbackQuery):
    text = algorithm_rus.rus_7(call.from_user.id)
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = call.message.text)
    await bot.send_message(call.from_user.id, text, reply_markup = rus_otv_keyboards.rus_7_pan)

# -------------- РУС 8
@dp.callback_query_handler(text = 'rus_8')
async def rus_8(call: types.CallbackQuery):
    text = algorithm_rus.rus_8(call.from_user.id)
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = call.message.text)
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = text, reply_markup = rus_otv_keyboards.rus_8_pan)

@dp.callback_query_handler(text = 'rus_8_1')
async def rus_8_1(call: types.CallbackQuery):
    text = algorithm_rus.rus_8(call.from_user.id)
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = call.message.text)
    await bot.send_message(call.from_user.id, text, reply_markup = rus_otv_keyboards.rus_8_pan)
    
# -------------- РУС 15
@dp.callback_query_handler(text = 'rus_15')
async def rus_15(call: types.CallbackQuery):
    text = algorithm_rus.rus_15(call.from_user.id)
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = call.message.text)
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = text, reply_markup = rus_otv_keyboards.rus_15_pan)

@dp.callback_query_handler(text = 'rus_15_1')
async def rus_15_1(call: types.CallbackQuery):
    text = algorithm_rus.rus_15(call.from_user.id)
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = call.message.text)
    await bot.send_message(call.from_user.id, text, reply_markup = rus_otv_keyboards.rus_15_pan)



# ------ НАЗАД ------
@dp.callback_query_handler(text = 'exit_1')
async def exit(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = call.message.text)
    await bot.send_message(call.from_user.id, bot_text.main, reply_markup = key.sc_pan)

@dp.callback_query_handler(text = 'exit')
async def exit(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, bot_text.main, reply_markup = key.sc_pan)

# ---------- Согласия -----------
@dp.callback_query_handler(text = 'sogl_t')
async def soglas(call: types.CallbackQuery):
    cursor.execute(f"""INSERT INTO users_bot(id, username) VALUES({call.from_user.id}, '{call.from_user.username}');""")
    cursor.execute(f"""INSERT INTO date_users(id, invite) VALUES({call.from_user.id}, '{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')}');""")
    cursor.execute(f"""INSERT INTO otvet_users(id) VALUES({call.from_user.id});""")
    await bot.edit_message_text(chat_id = call.from_user.id, message_id = call.message.message_id, text = bot_text.main, reply_markup = key.sc_pan)
    db.commit()

@dp.callback_query_handler(text='sub_ok')
async def sub_okk(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if check_sub_channel(await bot.get_chat_member(config.channelID, call.from_user.id)):
        info = cursor.execute('SELECT * FROM users_bot WHERE id=?', (call.from_user.id,))
        if info.fetchone() is None: 
            await bot.send_message(call.from_user.id, bot_text.start, reply_markup = key.sogl_pan)
            
        else: 
            await bot.send_message(call.from_user.id, bot_text.main, reply_markup = key.sc_pan)
    else:
        await bot.send_message(call.from_user.id, bot_text.No2_sub, reply_markup=key.sub)

# ------ Удалить сообщение ------
@dp.callback_query_handler(text = 'delete')
async def call_delete_menu(call: types.CallbackQuery): await bot.delete_message(call.message.chat.id, call.message.message_id)

# ------ КОНЕЦ ------
if __name__ == "__main__": executor.start_polling(dp, skip_updates = False)

