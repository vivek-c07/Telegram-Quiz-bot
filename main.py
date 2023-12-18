import os
from dotenv import load_dotenv

import datetime

import telebot
from telebot import types

#loading api token from env file
load_dotenv()
api_token = os.getenv('API_KEY')
bot = telebot.TeleBot(api_token)

#defining global variables
questions = [
    "What is the color of the sky?",
    "What is the national bird of India?",
    "What is the value of x , where x > 88 and x < 129?"
]

options = [
    ["Red", "Green", "Blue", "Orange"],
    ["Peacock", "Lion", "Lizard", "Tiger"],
    ["0", "2", "100", "NA"]
]

answers = [2, 0, 2]

name = ""
ids = []

#bot handlers and respective functions
@bot.message_handler(commands=['start'])
def open_covo(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Enter your name: ")
    @bot.message_handler(func=lambda message: True)
    def echo_message(message):
        global name

        name = message.text
        bot.send_message(chat_id, f"Hello {name}! Use /help to view available commands.")

@bot.message_handler(commands=['help'])
def help_return(message):
    chat_id = message.chat.id
    text1 = "Welcome to MCQ Practice Bot!\n"
    text2 = "Type /poll to attend quiz.\n"
    text3 = "Type /results to see results.\n"
    text4 = "Note: Ensure that you type /start so that your name is stored."
    text = text1+text2+text3+text4
    bot.send_message(chat_id, text)

@bot.message_handler(commands=["poll"])
def q1(message):
    for i in range(len(questions)):
        bot.send_poll(
            chat_id=message.chat.id,
            question=questions[i],
            options=options[i],
            type="quiz",
            correct_option_id=answers[i],
            is_anonymous=False,
        )

        @bot.poll_answer_handler()
        def handle_poll_answer(poll_answer):
            global ids
            
            #print(poll_answer)
            #print(poll_answer.option_ids[0], answers[i])
            ids.append([int(poll_answer.poll_id), int(poll_answer.option_ids[0])])

@bot.message_handler(commands=["results"])
def view_results(message):
    global name, ids

    chat_id = message.chat.id
    now = datetime.datetime.now()
    
    score = 0
    ids.sort(key=lambda x: x[0])
    for i in range(len(ids)):
        if ids[i][-1] == answers[i]:
            score += 1
    ids = []

    final_score = score/len(answers)*100
    status = "Fail"
    if final_score > 50:
        status = "Pass"

    bot.send_message(chat_id, f"Student: {name}")
    bot.send_message(chat_id, f"Time: {now.strftime("%d-%m-%Y %H:%M:%S")}")
    bot.send_message(chat_id, f"Score: {final_score}%")
    bot.send_message(chat_id, f"Status: {status}")

bot.infinity_polling()