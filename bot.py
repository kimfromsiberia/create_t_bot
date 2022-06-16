import logging
import datetime
import ephem
import csv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

all_cities = []
with open('ru_cities.csv', 'r') as file:
    csvfields = ['city_id', 'country_id', 'region_id', 'name']
    reader = csv.DictReader(file, csvfields, delimiter=';')
    for i in reader:
        all_cities.append(i['name'])

logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text('Привет, пользователь!')
    #print(update)

def talk_to_me(update, conetxe):
    text = update.message.text
    print(text)
    update.message.reply_text(text)

def planet_info(update, context):
    user_planet = update.message.text.split()
    user_planet = user_planet[1].lower().capitalize()
    today = str(datetime.date.today())
    planet_constellation = getattr(ephem, user_planet)(today)
    update.message.reply_text(ephem.constellation(planet_constellation))   

def wordcount(update, context):
    text = update.message.text.split()
    if len(text) < 2:
        update.message.reply_text('Nothing to count')
    else:
        update.message.reply_text(f'{len(text[1:])} words')

def fullmoon(update, context):
    today = str(datetime.date.today())
    full_moon = ephem.next_full_moon(today)
    update.message.reply_text(f'Next full moon {full_moon}')

def cities(update, context):

    if len(update.message.text.split()) < 2:
        update.message.reply_text("Don't forget to enter city")
        return
    else:    
        user_city = update.message.text.split()[1]
    if user_city not in all_cities:
        update.message.reply_text(f'{user_city} have been entered or doesnt exist')
    elif user_city in all_cities:
        all_cities.remove(user_city)
        reply_city = ''
        for city in all_cities:
            print(city)
            if user_city[-1].lower() == city[0].lower():
                reply_city = city
                all_cities.remove(city)
                update.message.reply_text(f'{reply_city}, your turn')
                break
        


def main():  # create t_bot
    mybot = Updater(settings.API_KEY, use_context = True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', planet_info))
    dp.add_handler(CommandHandler('wordcount', wordcount))
    dp.add_handler(CommandHandler('fullmoon', fullmoon))
    dp.add_handler(CommandHandler('cities', cities))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Start bot')
    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()