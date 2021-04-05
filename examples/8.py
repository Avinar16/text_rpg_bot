from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from dotenv import load_dotenv
import json
import os
import random

load_dotenv()
WAIT_ANSWER_STATE = 2


def load_test(filename):
    with open(filename, encoding="utf8") as f:
        tests = json.load(f)["test"]
        return tests


TEST = load_test("test.json")  # [{"question":"вопрос", "answer": "ответ"}, ...{...}]


def start(update, context):
    global TEST
    update.message.reply_text("Пожалуйста, пройдите опрос для проверки ваших знаний!.")
    random.shuffle(TEST)
    test_index = 0
    context.user_data["test_index"] = test_index
    context.user_data["right_answers"] = 0
    update.message.reply_text(TEST[test_index]['question'])
    return WAIT_ANSWER_STATE


def stop(update, content):
    update.message.reply_text("Жаль, что вы не смогли дойти до конца :(  Всего хорошего!")
    return ConversationHandler.END


def wait_answer(update, context):
    test_index = context.user_data["test_index"]
    answer = update.message.text
    right_answer = TEST[test_index]['answer']
    if answer.lower() == right_answer.lower():
        context.user_data["right_answers"] += 1
    test_index += 1
    if test_index == len(TEST):
        return test_end(update, context)
    else:
        context.user_data["test_index"] = test_index
        update.message.reply_text(TEST[test_index]['question'])
        return WAIT_ANSWER_STATE


def test_end(update, context):
    count = context.user_data["right_answers"]
    update.message.reply_text("Тест окончен!")
    update.message.reply_text(f"Вы набрали {count} из {len(TEST)}")
    update.message.reply_text("Если вы хотите пройти тест заново, нажмите /start")
    context.user_data.clear()
    return ConversationHandler.END


def main():
    updater = Updater(os.getenv("TOKEN"), use_context=True)
    dp = updater.dispatcher

    museum_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            WAIT_ANSWER_STATE: [MessageHandler(Filters.text, wait_answer, pass_user_data=True)],
        },
        fallbacks=[CommandHandler('stop', stop, pass_user_data=True)]
    )

    dp.add_handler(museum_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
