import telebot
import json
import random

TOKEN = "8093358460:AAG3LKKh5KjvspbQ4XuUY82zWTXVHBUuzLs"

bot = telebot.TeleBot(TOKEN)
with open("english.json", "r", encoding="utf-8") as e_json:
    user_data = json.load(e_json)


@bot.message_handler(commands=["start"])
def start(incoming_message):
    bot.send_message(incoming_message.chat.id, "Начнем обучение!")

@bot.message_handler(commands=["learn"])  #/learn 5
def learn(incoming_message):
    try:
        words_number = int(incoming_message.text.strip().lower().split()[1:][0])
        user_words = user_data.get(str(incoming_message.chat.id), {})
        bot.send_message(incoming_message.chat.id, "Я буду отправлять вам слова, ваша задача написать перевод!")
        ask_translation(incoming_message.chat.id, user_words, words_number)
    except:
        bot.send_message(incoming_message.chat.id, "Неверный формат команды.Введите команду в таком формате: /learn 5")

def ask_translation(id, dict, words_left):
    if words_left:
        words = list(dict.keys())
        word = random.choice(words)
        translate = dict.get(word, "")
        bot.send_message(id, f"Введите перевод для слова: {word}")
        bot.register_next_step_handler_by_chat_id(id, check_translate, translate, words_left)
    else:
        bot.send_message(id, "Изучение слов завершено!")

def check_translate(message, translate, words_left):
    user_words = user_data.get(str(message.chat.id), {})
    text = message.text.strip().lower()
    if text == translate:
        bot.send_message(message.chat.id, "Правильно!")
    else:
        bot.send_message(message.chat.id, "Ответ неверный!")
    words_left -= 1
    ask_translation(message.chat.id, user_words, words_left)

@bot.message_handler(commands=["help"])
def help(incoming_message):
    bot.send_message(incoming_message.chat.id, "Вот такие команды у нас есть: \n/learn (число) \n/add_word (word) (слово)")

@bot.message_handler(commands=["add_word"]) # /add_word apple яблоко
def add_word(incoming_message):
    chat_id = str(incoming_message.chat.id)
    try:
        text = incoming_message.text.strip().lower()
        text = text.split()[1:]
        if len(text) == 2:
            word, translate = text
        user_dict = user_data.get(chat_id, {})
        user_dict[word] = translate
        if not user_data[chat_id]:
            user_data[chat_id] = user_dict
        with open("english.json", "w", encoding="utf-8") as e_json:
            json.dump(user_data, e_json, ensure_ascii=False, indent=2)
        bot.send_message(chat_id, "Слово добавлено!")
    except:
        bot.send_message(incoming_message.chat.id, "Неверный формат команды.Введите команду в таком формате: /add_word apple яблоко")

bot.infinity_polling()