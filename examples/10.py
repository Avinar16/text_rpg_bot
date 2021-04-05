from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import requests
from dotenv import load_dotenv
import os

load_dotenv()

lang_keyboard = [['/ruen', '/enru']]
keyboard_markup = ReplyKeyboardMarkup(lang_keyboard, one_time_keyboard=False)
default_lang_pair = 'en|ru'


def start(update, context):
    update.message.reply_text("Приветствуем вас в сервисе переводчике!")
    update.message.reply_text("Я умею переводить с русского на английский и наоборот!")
    update.message.reply_text("Чтобы перевести текст, просто пришлите его мне!")
    update.message.reply_text("Если вы хотите сменить направление перевода, воспользуйтесь командами /ruen /enru",
                              reply_markup=keyboard_markup)
    context.user_data['lang_pair'] = default_lang_pair


def ru_en(update, context):
    context.user_data['lang_pair'] = 'ru|en'
    update.message.reply_text("Теперь вы переводите с русского на английский")


def en_ru(update, context):
    update.message.reply_text("Теперь вы переводите с английского на русский")
    context.user_data['lang_pair'] = 'en|ru'


def translate_api(lang_pair, text):
    url = "https://api.mymemory.translated.net/get"

    querystring = {"langpair": lang_pair, "q": text}

    response = requests.request("GET", url, params=querystring).json()

    return response["responseData"]["translatedText"]


def translate(update, context):
    lang_pair = context.user_data.get('lang_pair', default_lang_pair)
    text = update.message.text
    update.message.reply_text(translate_api(lang_pair, text), reply_markup=keyboard_markup)


def main():
    updater = Updater(os.getenv("TOKEN"), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ruen", ru_en))
    dp.add_handler(CommandHandler("enru", en_ru))
    dp.add_handler(MessageHandler(Filters.text, translate))
    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
