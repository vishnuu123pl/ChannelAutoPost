#    This file is part of the ChannelAutoForwarder distribution (https://github.com/xditya/ChannelAutoForwarder).
#    Copyright (c) 2021-2022 Aditya
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
#    License can be found in < https://github.com/xditya/ChannelAutoForwarder/blob/main/License> .

import logging
from telethon import TelegramClient, events, Button
from decouple import config

logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(message)s"
)
log = logging.getLogger("ChannelAutoPost")

# start the bot
log.info("Starting...")
try:
    apiid = config("APP_ID", cast=int)
    apihash = config("API_HASH")
    bottoken = config("BOT_TOKEN")
    frm = config("FROM_CHANNEL", cast=lambda x: [int(_) for _ in x.split(" ")])
    tochnls = config("TO_CHANNEL", cast=lambda x: [int(_) for _ in x.split(" ")])
    datgbot = TelegramClient(None, apiid, apihash).start(bot_token=bottoken)
except Exception as exc:
    log.error("Environment vars are missing! Kindly recheck.")
    log.info("Bot is quiting...")
    log.error(exc)
    exit()


@datgbot.on(events.NewMessage(pattern="/start"))
async def _(event):
    await event.reply(
        f"Hi `{event.sender.first_name}`!\n\n <b>മച്ചാനെ.. ഞാൻ വേറെ ലെവൽ BOT ഒന്നും അല്ല. പക്ഷെ നിങ്ങൾ മനുഷ്യൻമാരുടെ പണി രണ്ടിരട്ടി കുറക്കാൻ ഈ എന്നെ കൊണ്ട് സാധിക്കും. \n 🥅അത് കൊണ്ട് എന്നെയും എന്നെ ഉടമസ്താനെയും ബഹുമാച്ചിട്ടില്ലെങ്കിൽ ഞാൻ നിങ്ങൾക്ക് വേണ്ടി പണി എടുക്കത്തില്ല. \n \n എന്റെ ഉടമസ്ഥൻ 👉@Vis_hnu_Bot </b>",
        buttons=[
            Button.url("🤌 റോക്കി - ബാഹുബലി 😅", url="https://t.me/vis_hnu_bot"),
        ],
        link_preview=False,
    )


@datgbot.on(events.NewMessage(pattern="/help"))
async def helpp(event):
    await event.reply(
        "**Help**\n\n <b>മച്ചാനെ.. ഞാൻ വേറെ ലെവൽ BOT ഒന്നും അല്ല. പക്ഷെ നിങ്ങൾ മനുഷ്യൻമാരുടെ പണി രണ്ടിരട്ടി കുറക്കാൻ ഈ എന്നെ കൊണ്ട് സാധിക്കും. \n 🎗️അത് കൊണ്ട് എന്നെയും എന്നെ ഉടമസ്താനെയും ബഹുമാച്ചിട്ടില്ലെങ്കിൽ ഞാൻ നിങ്ങൾക്ക് വേണ്ടി പണി എടുക്കത്തില്ല. \n \n എന്റെ ഉടമസ്ഥൻ 👉@Vis_hnu_Bot:)</b> \n\n ☢️𝘛𝘏𝘈𝘕𝘟 𝘛𝘖 𝘍𝘐𝘓𝘌_𝘟1 𝘢𝘯𝘥 𝘞𝘖𝘙𝘓𝘋 𝘔𝘖𝘝𝘐𝘌𝘚."
    )


@datgbot.on(events.NewMessage(incoming=True, chats=frm))
async def _(event):
    for tochnl in tochnls:
        try:
            if event.poll:
                return
            if event.photo:
                photo = event.media.photo
                await datgbot.send_file(
                    tochnl, photo, caption=event.text, link_preview=False
                )
            elif event.media:
                try:
                    if event.media.webpage:
                        await datgbot.send_message(
                            tochnl, event.text, link_preview=False
                        )
                except Exception:
                    media = event.media.document
                    await datgbot.send_file(
                        tochnl, media, caption=event.text, link_preview=False
                    )
                finally:
                    return
            else:
                await datgbot.send_message(tochnl, event.text, link_preview=False)
        except Exception as exc:
            log.error(
                "TO_CHANNEL ID is wrong or I can't send messages there (make me admin).\nTraceback:\n%s",
                exc,
            )


log.info("Bot has started.")
log.info("Do visit https://xditya.me !")
datgbot.run_until_disconnected()
