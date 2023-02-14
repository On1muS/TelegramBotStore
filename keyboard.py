from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

admin_kb = ReplyKeyboardMarkup(resize_keyboard = True)
admin_kb.add(KeyboardButton('/mailing')).add(KeyboardButton('/create_new_order')).add(KeyboardButton('/add_new_admin')).add(KeyboardButton('/view_admins')).add(KeyboardButton('Go back to user panel'))

user_a_kb = ReplyKeyboardMarkup(resize_keyboard = True)
user_a_kb.add(KeyboardButton('View orders 📲')).add(KeyboardButton('Change language 🏳️')).add(KeyboardButton('View admin panel 🎟'))

user_kb = ReplyKeyboardMarkup(resize_keyboard = True)
user_kb.add(KeyboardButton('View orders 📲')).add(KeyboardButton('Change language 🏳️')).add(KeyboardButton('Write to administration ⚒'))
