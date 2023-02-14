from keyboard import user_kb, admin_kb, user_a_kb
from create_bot import dp, bot
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from database import db


async def on_Start(message: types.Message):
    global admin_list
    admin_list = await db.get_admins()
    if message.from_user.id in admin_list:
        await db.add_user(message.from_user.id, message.from_user.username)
        await message.reply('Bot started', reply_markup=user_a_kb)
    else:
        await db.add_user(message.from_user.id, message.from_user.username)
        await message.reply('Bot started', reply_markup=user_kb)


class FSMAdmin(StatesGroup):
    text = State()
    photo = State()

async def Mailing(message: types.Message):
    if message.from_user.id in admin_list:
        await FSMAdmin.text.set()
        await bot.send_message(message.from_user.id, 'Enter mailing`s text', reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Cancel', callback_data = 'cancel')))
        await message.delete()


async def Mailing_text(message: types.Message, state: FSMAdmin):
    async with state.proxy() as data:
        data['text'] = message.text
    await FSMAdmin.next()
    await bot.send_message(message.from_user.id, 'Send the photo of mailing', reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Send without photo', callback_data = 'no_photo'), InlineKeyboardButton('Cancel', callback_data = 'cancel')))

async def Mailing_photo(message: types.Message, state: FSMAdmin):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    
    async with state.proxy() as data:
        photo = data.get('photo')
        text = data.get('text')
        user_list = await db.get_users()
        print(user_list)
        try:
            for i in user_list:
                await bot.send_photo(i, photo = photo, caption = f"<b>New Mailing</b>\n\n{text}", parse_mode="HTML")
        except Exception:
            pass
    
    await state.finish()
    await bot.send_message(message.from_user.id, 'Sucsessfull')

@dp.callback_query_handler(text = 'no_photo', state = '*')
async def no_photo_mailing(message: types.Message, state: FSMAdmin):
    async with state.proxy() as data:
        text = data.get('text')
        user_list = await db.get_users()
        try:
            for i in user_list:
                await bot.send_message(i, f"<b>New Mailing</b>\n\n{text}", parse_mode="HTML")
        except Exception:
            pass
    await state.finish()
    await bot.send_message(message.from_user.id, 'Sucsessful')

@dp.callback_query_handler(text = 'cancel', state = '*')
async def chancel_mailing(message: types.Message, state: FSMAdmin):
    current_state = state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id, 'Cancelled')


class FSMAddNewAdmin(StatesGroup):
    chat_id = State()
    surname_and_name = State()

async def add_new_admin(message: types.Message):
    if message.from_user.id in admin_list:
        await FSMAddNewAdmin.chat_id.set()
        await bot.send_message(message.from_user.id, 'Enter new admin`s chat_id (Google how to know telegram chat id)', reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Cancel', callback_data = 'cancel')))
        await message.delete()


async def add_new_admin_chat_id(message: types.Message, state: FSMAddNewAdmin):
    async with state.proxy() as data:
        data['chat_id'] = message.text
    await FSMAddNewAdmin.next()
    await bot.send_message(message.from_user.id, 'Enter the name and surname of new admin', reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Cancel', callback_data = 'cancel')))

async def add_new_admin_name_and_surname(message: types.Message, state: FSMAddNewAdmin):
    async with state.proxy() as data:
        data['surname_and_name'] = message.text
    
    async with state.proxy() as data:
        chat_id = data.get('chat_id')
        name_and_surname = data.get('surname_and_name')
        await db.add_admin(chat_id, name_and_surname)
        await bot.send_message(message.from_user.id, f'New admin was added')
    
    await state.finish()
    await bot.send_message(message.from_user.id, 'Sucsessfull')

@dp.callback_query_handler(text = 'cancel', state = '*')
async def chancel_mailing(message: types.Message, state: FSMAdmin):
    current_state = state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id, 'Cancelled')


class CreateNewOrder(StatesGroup):
    title = State()
    text = State()
    price = State()
    photo = State()

async def create_new_order(message: types.Message):
    if message.from_user.id in admin_list:
        await CreateNewOrder.title.set()
        await bot.send_message(message.from_user.id, "Enter the title of order", reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Cancel', callback_data = 'cancel')))
        await message.delete()


async def add_title_to_order(message: types.Message, state: CreateNewOrder):
    async with state.proxy() as data:
        data['title'] = message.text
    await CreateNewOrder.next()
    await bot.send_message(message.from_user.id, 'Enter the text of order', reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Cancel', callback_data = 'cancel')))

async def add_text_to_order(message: types.Message, state: CreateNewOrder):
    async with state.proxy() as data:
        data['text'] = message.text
    await CreateNewOrder.next()
    await bot.send_message(message.from_user.id, 'Send the price of order (also indicate the currency)', reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Cancel', callback_data = 'cancel')))

async def add_price_to_order(message: types.Message, state: CreateNewOrder):
    async with state.proxy() as data:
        data['price'] = message.text
    await CreateNewOrder.next()
    await bot.send_message(message.from_user.id, 'Send the photo of order', reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Cancel', callback_data = 'cancel')))

async def add_photo_to_order(message: types.Message, state: CreateNewOrder):
    async with state.proxy() as data:
        try:
            data['photo'] = message.photo[0].file_id
            title = data.get('title')
            text = data.get('text')
            price = data.get('price')
            photo = data.get('photo')
            await db.add_order(title, text, price, photo)
            user_list = await db.get_users()
            for user in user_list:
                await bot.send_photo(user, photo = photo, caption = f'There is a new order in the shop\n<b>{title}</b>\n{text}\nPrice: {price}', parse_mode="html")
            await state.finish()
        except Exception:
            await message.reply('Wrong data')

@dp.callback_query_handler(text = 'cancel', state = '*')
async def chancel_order(message: types.Message, state: CreateNewOrder):
    current_state = state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id, 'Cancelled')

async def admin_functions(message: types.Message):
    admin_list = await db.get_admins()
    global msg
    if message.from_user.id in admin_list:
        if message.text == 'View admin panel 🎟' and message.from_user.id in admin_list:
            await bot.send_message(message.from_user.id, 'Administrator mode was activated', reply_markup = admin_kb)
            await message.delete()
        if message.text == 'Go back to user panel' and message.from_user.id in admin_list:
            await bot.send_message(message.from_user.id, 'Administration mode was deactivated', reply_markup = user_a_kb)
            await message.delete()
        if message.text == 'View orders 📲':
            global order_list, len_orders, need_element
            order_list = await db.get_orders()
            len_orders = len(order_list)
            need_element = 0
            if len_orders == 0:
                await bot.send_message(message.from_user.id, 'There are no orders in the shop')
                await message.delete()
            else:
                msg = await bot.send_photo(message.from_user.id, photo = order_list[need_element][3], caption = f'<b>{order_list[need_element][0]}</b>\n{order_list[need_element][1]}\nPrice: {order_list[need_element][2]}', parse_mode = 'HTML', reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton(text = '<', callback_data = 'back'), InlineKeyboardButton(text = '>', callback_data = 'next')).add(InlineKeyboardButton(text = f'{need_element + 1}', callback_data = 'None'), InlineKeyboardButton(text = f'/', callback_data = 'None'), InlineKeyboardButton(text = f'{len_orders}', callback_data = 'None')).add(InlineKeyboardButton(text = '<<', callback_data = 'to_start'), InlineKeyboardButton(text = '>>', callback_data = 'to_end')).add(InlineKeyboardButton(text = 'Delete', callback_data = 'delete_order')))
                await message.delete()
    else:
        if message.text == 'View admin panel 🎟':
            await message.reply('You are not an admin')
            await message.delete()
        if message.text == 'Go back to user panel':
            await message.reply('You are not an admin')
            await message.delete()
        if message.text == 'View orders 📲':
            order_list = await db.get_orders()
            len_orders = len(order_list)
            need_element = 0
            if len_orders == 0:
                await bot.send_message(message.from_user.id, 'There are no orders in the shop')
                await message.delete()
            else:
                msg = await bot.send_photo(message.from_user.id, photo = order_list[need_element][3], caption = f'<b>{order_list[need_element][0]}</b>\n{order_list[need_element][1]}\nPrice: {order_list[need_element][2]}', parse_mode = 'HTML', reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton(text = '<', callback_data = 'user_back'), InlineKeyboardButton(text = '>', callback_data = 'user_next')).add(InlineKeyboardButton(text = f'{need_element + 1}', callback_data = 'None'), InlineKeyboardButton(text = f'/', callback_data = 'None'), InlineKeyboardButton(text = f'{len_orders}', callback_data = 'None')).add(InlineKeyboardButton(text = '<<', callback_data = 'user_to_start'), InlineKeyboardButton(text = '>>', callback_data = 'user_to_end')))
                await message.delete()

# Callbacks to users

@dp.callback_query_handler(text = 'user_next')
async def next_order(callback_query: types.CallbackQuery):
    global need_element
    if need_element < len_orders - 1:
        need_element += 1
        await callback_query.message.delete()
        await bot.send_photo(callback_query.message.chat.id, photo=order_list[need_element][3],
                                   caption=f'<b>{order_list[need_element][0]}</b>\n{order_list[need_element][1]}\nPrice: {order_list[need_element][2]}',
                                   parse_mode='HTML', reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(text='<', callback_data='user_back'),
                InlineKeyboardButton(text='>', callback_data='user_next')).add(
                InlineKeyboardButton(text=f'{need_element + 1}', callback_data='None'),
                InlineKeyboardButton(text=f'/', callback_data='None'),
                InlineKeyboardButton(text=f'{len_orders}', callback_data='None')).add(
                InlineKeyboardButton(text='<<', callback_data='user_to_start'),
                InlineKeyboardButton(text='>>', callback_data='user_to_end')))

@dp.callback_query_handler(text = 'user_back')
async def next_order(callback_query: types.CallbackQuery):
    global need_element
    if need_element > 0:
        need_element -= 1
        await callback_query.message.delete()
        await bot.send_photo(callback_query.message.chat.id, photo=order_list[need_element][3],
                                   caption=f'<b>{order_list[need_element][0]}</b>\n{order_list[need_element][1]}\nPrice: {order_list[need_element][2]}',
                                   parse_mode='HTML', reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(text='<', callback_data='user_back'),
                InlineKeyboardButton(text='>', callback_data='user_next')).add(
                InlineKeyboardButton(text=f'{need_element + 1}', callback_data='None'),
                InlineKeyboardButton(text=f'/', callback_data='None'),
                InlineKeyboardButton(text=f'{len_orders}', callback_data='None')).add(
                InlineKeyboardButton(text='<<', callback_data='user_to_start'),
                InlineKeyboardButton(text='>>', callback_data='user_to_end')))

@dp.callback_query_handler(text = 'user_to_end')
async def next_order(callback_query: types.CallbackQuery):
    global need_element
    need_element = len_orders - 1
    await callback_query.message.delete()
    await bot.send_photo(callback_query.message.chat.id, photo=order_list[need_element][3],
                               caption=f'<b>{order_list[need_element][0]}</b>\n{order_list[need_element][1]}\nPrice: {order_list[need_element][2]}',
                               parse_mode='HTML', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(text='<', callback_data='user_back'),
            InlineKeyboardButton(text='>', callback_data='user_next')).add(
            InlineKeyboardButton(text=f'{need_element + 1}', callback_data='None'),
            InlineKeyboardButton(text=f'/', callback_data='None'),
            InlineKeyboardButton(text=f'{len_orders}', callback_data='None')).add(
            InlineKeyboardButton(text='<<', callback_data='user_to_start'),
            InlineKeyboardButton(text='>>', callback_data='user_to_end')))

@dp.callback_query_handler(text = 'user_to_start')
async def next_order(callback_query: types.CallbackQuery):
    global need_element
    need_element = 0
    await callback_query.message.delete()
    await bot.send_photo(callback_query.message.chat.id, photo=order_list[need_element][3],
                               caption=f'<b>{order_list[need_element][0]}</b>\n{order_list[need_element][1]}\nPrice: {order_list[need_element][2]}',
                               parse_mode='HTML', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(text='<', callback_data='user_back'),
            InlineKeyboardButton(text='>', callback_data='user_next')).add(
            InlineKeyboardButton(text=f'{need_element + 1}', callback_data='None'),
            InlineKeyboardButton(text=f'/', callback_data='None'),
            InlineKeyboardButton(text=f'{len_orders}', callback_data='None')).add(
            InlineKeyboardButton(text='<<', callback_data='user_to_start'),
            InlineKeyboardButton(text='>>', callback_data='user_to_end')))





# Callbacks for admins
@dp.callback_query_handler(text = 'next')
async def next_order(callback_query: types.CallbackQuery):
    global need_element
    if need_element < len_orders - 1:
        need_element += 1
        await callback_query.message.delete()
        await bot.send_photo(callback_query.message.chat.id, photo=order_list[need_element][3],
                                   caption=f'<b>{order_list[need_element][0]}</b>\n{order_list[need_element][1]}\nPrice: {order_list[need_element][2]}',
                                   parse_mode='HTML', reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(text='<', callback_data='back'),
                InlineKeyboardButton(text='>', callback_data='next')).add(
                InlineKeyboardButton(text=f'{need_element + 1}', callback_data='None'),
                InlineKeyboardButton(text=f'/', callback_data='None'),
                InlineKeyboardButton(text=f'{len_orders}', callback_data='None')).add(
                InlineKeyboardButton(text='<<', callback_data='to_start'),
                InlineKeyboardButton(text='>>', callback_data='to_end')).add(
                InlineKeyboardButton(text='Delete', callback_data='delete_order')))

@dp.callback_query_handler(text = 'back')
async def next_order(callback_query: types.CallbackQuery):
    global need_element
    if need_element > 0:
        need_element -= 1
        await callback_query.message.delete()
        await bot.send_photo(callback_query.message.chat.id, photo=order_list[need_element][3],
                                   caption=f'<b>{order_list[need_element][0]}</b>\n{order_list[need_element][1]}\nPrice: {order_list[need_element][2]}',
                                   parse_mode='HTML', reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(text='<', callback_data='back'),
                InlineKeyboardButton(text='>', callback_data='next')).add(
                InlineKeyboardButton(text=f'{need_element + 1}', callback_data='None'),
                InlineKeyboardButton(text=f'/', callback_data='None'),
                InlineKeyboardButton(text=f'{len_orders}', callback_data='None')).add(
                InlineKeyboardButton(text='<<', callback_data='to_start'),
                InlineKeyboardButton(text='>>', callback_data='to_end')).add(
                InlineKeyboardButton(text='Delete', callback_data='delete_order')))

@dp.callback_query_handler(text = 'to_end')
async def next_order(callback_query: types.CallbackQuery):
    global need_element
    need_element = len_orders - 1
    await callback_query.message.delete()
    await bot.send_photo(callback_query.message.chat.id, photo=order_list[need_element][3],
                               caption=f'<b>{order_list[need_element][0]}</b>\n{order_list[need_element][1]}\nPrice: {order_list[need_element][2]}',
                               parse_mode='HTML', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(text='<', callback_data='back'),
            InlineKeyboardButton(text='>', callback_data='next')).add(
            InlineKeyboardButton(text=f'{need_element + 1}', callback_data='None'),
            InlineKeyboardButton(text=f'/', callback_data='None'),
            InlineKeyboardButton(text=f'{len_orders}', callback_data='None')).add(
            InlineKeyboardButton(text='<<', callback_data='to_start'),
            InlineKeyboardButton(text='>>', callback_data='to_end')).add(
            InlineKeyboardButton(text='Delete', callback_data='delete_order')))

@dp.callback_query_handler(text = 'to_start')
async def next_order(callback_query: types.CallbackQuery):
    global need_element
    need_element = 0
    await callback_query.message.delete()
    await bot.send_photo(callback_query.message.chat.id, photo=order_list[need_element][3],
                               caption=f'<b>{order_list[need_element][0]}</b>\n{order_list[need_element][1]}\nPrice: {order_list[need_element][2]}',
                               parse_mode='HTML', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(text='<', callback_data='back'),
            InlineKeyboardButton(text='>', callback_data='next')).add(
            InlineKeyboardButton(text=f'{need_element + 1}', callback_data='None'),
            InlineKeyboardButton(text=f'/', callback_data='None'),
            InlineKeyboardButton(text=f'{len_orders}', callback_data='None')).add(
            InlineKeyboardButton(text='<<', callback_data='to_start'),
            InlineKeyboardButton(text='>>', callback_data='to_end')).add(
            InlineKeyboardButton(text='Delete', callback_data='delete_order')))

@dp.callback_query_handler(text = 'delete_order')
async def delete_order(message: types.Message):
    global order_list, need_element
    await db.delete_order(order_list[need_element][0])
    await bot.send_message(message.from_user.id, 'Deleted sucsessful')
    order_list = await db.get_orders()


async def view_admins(message: types.Message):
    admin_list = await db.get_admins()
    if message.from_user.id in admin_list:
        admin_names_list = await db.get_admins_names()
        await message.delete()
        await bot.send_message(message.from_user.id, '------------------------------------------------------')
        for i in admin_names_list:
            await bot.send_message(message.from_user.id, f'{i}', reply_markup=ReplyKeyboardMarkup().add(KeyboardButton('/delete_admin')).add(KeyboardButton('/go_back_to_admin_panel')))
        await bot.send_message(message.from_user.id, '------------------------------------------------------')



class DeleteAdmin(StatesGroup):
    username = State()

async def name_of_admin(message: types.Message):
    admin_list = await db.get_admins()
    if message.from_user.id in admin_list:
        await DeleteAdmin.username.set()
        await bot.send_message(message.from_user.id, "Enter the name and the surname of admin", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text = 'Cancel', callback_data = 'cancel')))
        await message.delete()


async def delete_admin(message: types.Message, state: DeleteAdmin):
        async with state.proxy() as data:
            data['username'] = message.text
            name_and_surname = data.get('username')
            a = await db.delete_admin(name_and_surname)
            await bot.send_message(message.from_user.id, f'{a}', reply_markup=admin_kb)
            await state.finish()

@dp.callback_query_handler(text = 'cancel', state = '*')
async def chancel_order(message: types.Message, state: CreateNewOrder):
    current_state = state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id, 'Cancelled', reply_markup = admin_kb)

async def go_back_to_admin_panel(message: types.Message):
    await bot.send_message(message.from_user.id, 'OK', reply_markup=admin_kb)
    await message.delete()

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(on_Start, commands=['start'])
    dp.register_message_handler(go_back_to_admin_panel, commands=['go_back_to_admin_panel'])
    dp.register_message_handler(name_of_admin, commands='delete_admin', state = None)
    dp.register_message_handler(delete_admin, state=DeleteAdmin.username)
    dp.register_message_handler(view_admins, commands=['view_admins'])
    dp.register_message_handler(create_new_order, commands = ['create_new_order'], state = None)
    dp.register_message_handler(add_title_to_order, state = CreateNewOrder.title)
    dp.register_message_handler(add_text_to_order, state = CreateNewOrder.text)
    dp.register_message_handler(add_price_to_order, state = CreateNewOrder.price)
    dp.register_message_handler(add_photo_to_order, state = CreateNewOrder.photo, content_types=['photo'])
    dp.register_message_handler(add_new_admin, commands = ['add_new_admin'], state = None)
    dp.register_message_handler(add_new_admin_chat_id, state = FSMAddNewAdmin.chat_id)
    dp.register_message_handler(add_new_admin_name_and_surname, state = FSMAddNewAdmin.surname_and_name)
    dp.register_message_handler(Mailing, commands = ['mailing'], state = None)
    dp.register_message_handler(Mailing_text, state = FSMAdmin.text)
    dp.register_message_handler(Mailing_photo, state = FSMAdmin.photo, content_types=['photo'])
    dp.register_message_handler(admin_functions)
