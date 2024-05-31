import telebot
from config import config
from database import convertor, connect
from mssql import get_info
from site_parser import site_parser


bot = telebot.TeleBot(f"{config.TOKEN}")
url = 'https://library.bsuir.by'

@bot.message_handler(commands=['start'])
def start(message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    user_name = message.from_user.username
    user_fullname = f'{first_name} {last_name}' if first_name and last_name is None else user_name
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    button_site = telebot.types.InlineKeyboardButton('💻 Сайт Библиотеки', url='https://library.bsuir.by/')
    button_rep = telebot.types.InlineKeyboardButton('📑 Репозиторий', url='https://libeldoc.bsuir.by/')
    button_catalog = telebot.types.InlineKeyboardButton('📚 Каталог', url='https://books.bsuir.by/MegaPro/web')

    markup.add(button_site, button_rep, button_catalog)

    bot.send_message(message.chat.id, f'Привет ✌️, <strong>{user_fullname}.</strong>\n'
                                      f'Тебя приветсвует Библиотека БГУИР📘.\n'
                                      f'Напиши /help, чтобы узнать, что я умею.', reply_markup=markup, parse_mode="HTML")


# @bot.message_handler(commands=['news'])
# def get_news(message, page=1, previous_message=None):
#
#     markup = telebot.types.InlineKeyboardMarkup()
#     try:
#         news_list = site_parser.parse_news()
#         print(news_list[6:])
#         left = page - 1 if page != 1 else len(news_list)
#         right = page + 1 if page != len(news_list) else 1
#
#         left_btn = telebot.types.InlineKeyboardButton('👈', callback_data=f'to {left}')
#         page_btn = telebot.types.InlineKeyboardButton(f'{str(page)}/{str(len(news_list))}', callback_data='None')
#         right_btn = telebot.types.InlineKeyboardButton('👉', callback_data=f'to {right}')
#         order_btn = telebot.types.InlineKeyboardButton('Читать', url=news_list[page - 1]["news_url"])
#         markup.add(left_btn, page_btn, right_btn)
#         markup.add(order_btn)
#         msg = f'<strong>{news_list[page - 1]["title"]}</strong>'
#         # bot.send_photo(message.chat.id, photo=news_list[page - 1]['img'], caption=msg,
#         #                reply_markup=markup,
#         #                parse_mode="HTML")
#
#         bot.send_message(message.chat.id, text=msg,reply_markup=markup, parse_mode="HTML")
#
#         # bot.send_message(message.chat.id, 'Свежие новости 📰', reply_markup=markup.add(*btn_list))
#     except:
#         bot.send_message(message.chat.id, 'Ошибка подключения')
#         raise ConnectionError
#
#     try: bot.delete_message(message.chat.id, previous_message.id)
#     except: pass

# @bot.callback_query_handler(func=lambda call: True)
# def process_callback_button1(call):
#     if 'to' in call.data:
#         page = int(call.data.split(' ')[1])
#         get_news(call.message, page=page, previous_message=call.message)

@bot.message_handler(commands=['debt'])
def get_debt(message):
    send = bot.send_message(message.chat.id, 'Введите номер <strong>читательского билета</strong>', parse_mode="HTML")
    bot.register_next_step_handler(send, get_user_by_id)

def get_user_by_id(message):
    user_list_debt = get_info.get_debt_user(message.text)

    output_list = []

    if not user_list_debt:
        bot.send_message(message.chat.id, '<strong>У вас нет задолжностей!</strong>', parse_mode="HTML")
        return

    for item in user_list_debt:
        output_list.append(f'{item.get("BOOK")}\n')


    msg = "\n".join(output_list)

    chunk_size = len(msg) // 4096

    if(len(msg) / 4096 > 1):
        chunks = [output_list[i:i + chunk_size] for i in range(0, len(output_list), chunk_size)]
        for item in chunks:
            bot.send_message(message.chat.id, text="\n".join(item), parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, text=msg, parse_mode="HTML")




@bot.message_handler(content_types=['text'])
def get_list_books(message):
    user_list = convertor.tuple_to_dict(user_str=message.text)[:10]
    output_list = []

    if not user_list:
        bot.send_message(message.chat.id, f'Книги с таким названием <strong>{message.text}</strong> у нас нет', parse_mode="HTML")
        return

    for item in user_list:
        output_list.append(f'<strong>{item.get("author")}|{item.get("year")}</strong>\n<a href="{item.get("url")}">{item.get("name")}</a>\n')


    msg =  "\n".join(output_list)

    bot.send_message(message.chat.id, text=msg, parse_mode="HTML")

    print(bot.get_chat_member(message.chat.id, message.from_user.id))




if __name__ == '__main__':
    bot.infinity_polling()
