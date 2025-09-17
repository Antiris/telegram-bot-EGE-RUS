from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# Реализованы только 4 5 6 7 8 15 номера. потому что для других номеров бы ушло много времени для написания их логики 
rus_types = InlineKeyboardMarkup()
rus_4 = InlineKeyboardButton('4', callback_data='rus_4')
rus_5 = InlineKeyboardButton('5', callback_data='rus_5')
rus_6 = InlineKeyboardButton('6', callback_data='rus_6')
rus_7 = InlineKeyboardButton('7', callback_data='rus_7')
rus_8 = InlineKeyboardButton('8', callback_data='rus_8')
rus_15 = InlineKeyboardButton('15', callback_data='rus_15')
exit = InlineKeyboardButton('Назад ↩️', callback_data = 'exit')
rus_pan = rus_types.add(rus_4, rus_5, rus_6).add(rus_7, rus_8, rus_15, exit)

