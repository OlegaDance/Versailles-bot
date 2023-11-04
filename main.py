import telebot
import webbrowser
from telebot import types
import re

waiting_for_phone = {}  # Словник для збереження стану очікування номера телефону
user_phone = {}  # Словник для збереження номерів телефонів користувачів

bot = telebot.TeleBot('6657330380:AAHtfeCcno4rtsoXY7BuGnzPM28MjkZgo4o')

@bot.message_handler(commands=['site','link'])
def site(message):
    webbrowser.open('https://translate.google.com/?sl=en&tl=uk&op=translate')


@bot.message_handler(commands=['start'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton('Перейти на сайт', url='https://translate.google.com/?sl=en&tl=uk&op=translate'))

    row2 = []
    row2.append(types.InlineKeyboardButton('Так', callback_data='yes'))
    row2.append(types.InlineKeyboardButton('Ні', callback_data='no'))
    markup.add(*row2)

    @bot.message_handler(commands=['start'])
    def main(message):
        bot.send_message(message.chat.id, f'Привіт! {message.from_user.first_name}, Ви зареєстровані на нашому сайті?',
                         reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data == 'yes')
    def yes_callback(query):
        chat_id = query.message.chat.id
        bot.send_message(chat_id, "Введіть свій номер телефону.")
        waiting_for_phone[chat_id] = True  # Встановлюємо стан очікування номера телефону

    @bot.message_handler(func=lambda message: waiting_for_phone.get(message.chat.id, False))
    def phone_callback(message):
        chat_id = message.chat.id
        phone_number = message.text

        # Перевірка, що введений номер містить тільки цифри
        if re.match(r"^\d+$", phone_number):
            user_phone[chat_id] = phone_number  # Зберігаємо номер телефону в словнику user_phone

            # Створюємо InlineKeyboard для "Редагувати" і "Підтвердити"
            edit_confirm_markup = types.InlineKeyboardMarkup()
            edit_confirm_markup.row(
                types.InlineKeyboardButton('Редагувати', callback_data='edit'),
                types.InlineKeyboardButton('Підтвердити', callback_data='confirm')
            )

            bot.send_message(chat_id, f"Ви ввели номер телефону: {phone_number}", reply_markup=edit_confirm_markup)
            waiting_for_phone[chat_id] = False  # Завершуємо очікування номера телефону
        else:
            bot.send_message(chat_id, "Введений номер повинен містити тільки цифри. Спробуйте ще раз.")

    @bot.callback_query_handler(func=lambda call: call.data == 'edit')
    def edit_phone(query):
        chat_id = query.message.chat.id
        bot.send_message(chat_id, "Введіть новий номер телефону.")
        waiting_for_phone[chat_id] = True  # Встановлюємо стан очікування нового номера телефону

    @bot.callback_query_handler(func=lambda call: call.data == 'confirm')
    def confirm_phone(query):
        chat_id = query.message.chat.id
        phone_number = user_phone.get(chat_id)
        bot.send_message(chat_id, f"Підтверджено номер телефону почикайте поки я шукаю вас в своїх даних...")
        waiting_for_phone[chat_id] = False  # Завершуємо очікування номера телефону

    @bot.callback_query_handler(func=lambda call: call.data == 'no')
    def no_callback(query):
        chat_id = query.message.chat.id
        bot.send_message(chat_id, "Зареєструйтесь на нашому сайті щоб продовжити")

        auth = types.InlineKeyboardMarkup()
        auth.add(
            types.InlineKeyboardButton('Перейти на сайт', url='https://translate.google.com/?sl=en&tl=uk&op=translate'))

        bot.send_message(chat_id, "Для реєстрації перейдіть за посиланням:", reply_markup=auth)

    @bot.message_handler(func=lambda message: message.text == 'Так')
    def text_callback(message):
        bot.send_message(message.chat.id, "Ви натиснули кнопку 'Так'. Ось ваше повідомлення.")

    @bot.message_handler(commands=['start'])
    def main(message):
        bot.send_message(message.chat.id, f'Привіт! {message.from_user.first_name}, Ви зареєстровані на нашому сайті?',
                         reply_markup=markup)

    bot.send_message(message.chat.id, f'Привіт! {message.from_user.first_name}, Ви зареєстровані на нашому сайті?',
                     reply_markup=markup)



@bot.message_handler(content_types=['photo'])
def get_photo(message):
    bot.reply_to(message,'Яка красива фотографія ! але навіщо вона мені ?')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Доступні команди:\n'
                                      '/start - Почати чат\n'
                                      '/site або /link - Перейти на сайт\n'
                                      '/help - Отримати довідку')

bot.polling(none_stop=True)
