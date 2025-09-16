from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ====== СОГЛАШЕНИЕ ======
sogltypes = InlineKeyboardMarkup()
sogl = InlineKeyboardButton('✅ Согласен', callback_data = 'sogl_t')
sogl_pan = sogltypes.add(sogl)

# ====== ПРЕДМЕТЫ ВЫБОР ======
schoolworks = InlineKeyboardMarkup()
rus_works = InlineKeyboardButton('Русский язык 📖', callback_data = 'rus_types')
sc_pan = schoolworks.add(rus_works)

# Удалить
call_delete = InlineKeyboardMarkup()
delete = InlineKeyboardButton('Понятно ✅', callback_data = 'delete')
rulesdelete = call_delete.add(delete)

#Подписка
call_sub = InlineKeyboardMarkup()
sub_link = InlineKeyboardButton(text='Подписаться 🔥', url='t.me/sdadim_ege')
sub_ok = InlineKeyboardButton(text='Я подписчик 😎', callback_data='sub_ok')
sub = call_sub.add(sub_link).add(sub_ok)