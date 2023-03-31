import openai as ai
import telebot as tb
import os
import dotenv

dotenv.load_dotenv('.env')
history_file_path = os.path.abspath(os.path.join('TbHistory.txt'))

ai_api_key = os.environ['ai_api_key']
bot_api_key = os.environ['DaVinci_bot_api_key']

ai.api_key = ai_api_key
bot = tb.TeleBot(bot_api_key)


@bot.message_handler(func=lambda message: True)
def handle_message(message: classmethod) -> None:
    with open(history_file_path, 'a', encoding='utf=8') as file:
        file.write(f'USER {message.from_user.first_name}: {message.text}'+'\n')

    response = ai.Completion.create(
        model='text-davinci-003',
        prompt=message.text,
        temperature=0.5,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0
    )

    bot.send_message(chat_id=message.from_user.id, text=''.join(response['choices'][0]['text']))



bot.polling(none_stop=True)
