from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
from api import tess_api, simbad_api

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token=os.environ.get("SIMTESS_BOT"), use_context=True)
dispatcher = updater.dispatcher

# ========================================================
#                          Commands
# ========================================================

def info(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, \
                            text="Hi! Give me TESS or SIMBAD target and,\n" +
                                 "I will tell you their RA/DEC")

info_handler = CommandHandler('info', info)
dispatcher.add_handler(info_handler)    

def source(update, context):
    print(context.args)
    if not context.args:
        context.bot.send_message(chat_id=update.effective_chat.id, \
                            text="Usage: /source <target-id>\n" +
                                  "eg: /source toi1005")
        return

    planet_name = context.args[0].lower()
    planet_name = planet_name.strip()

    planet_details = None
    if planet_name[:3] == "toi":
        planet_details = tess_api.get_planet_data([planet_name])
    elif planet_name[:2] == "hd":
        planet_details = simbad_api.get_planet_data([planet_name])

    if planet_details:
        planet_details = planet_details[0]
        planet_details = "Target Name:    {}\nRA:    {}\nDEC:    {}".format(\
                                                                    planet_details[0],\
                                                                    planet_details[1],\
                                                                    planet_details[2])
    else:
        planet_details = "Invalid Target Name!"

    context.bot.send_message(chat_id=update.effective_chat.id, \
                            text=planet_details)

source_handler = CommandHandler('source', source)
dispatcher.add_handler(source_handler)

# ========================================================


# ========================================================
#                   Message Hanlders
# ========================================================
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, \
                            text="Doesn't look like anything to me!")

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)
# ========================================================


updater.start_polling()