from asyncio import sleep
import requests
from googletrans import LANGUAGES, Translator
from jepthon import jepiq
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import soft_deEmojify


async def gtrans(text, lan):
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
    payload = f"q={text}&target={lan}"
    headers = {
	    "content-type": "application/x-www-form-urlencoded",
	    "Accept-Encoding": "application/gzip",
	    "X-RapidAPI-Key": "c9ff429aa1mshf8fcb2a0f899802p108b4ejsna4a57732c397",
	    "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    if response["error"].code == 400:
        return Flase
    return [response["translatedText"], response("detectedSourceLanguage")]

@jepiq.ar_cmd(
    pattern="ترجمة ([\s\S]*)",
    command=("ترجمة", "tools"),
    info={
        "header": "To translate the text to required language.",
        "note": "For langugage codes check [this link](https://bit.ly/2SRQ6WU)",
        "usage": [
            "{tr}tl <language code> ; <text>",
            "{tr}tl <language codes>",
        ],
        "examples": "{tr}tl te ; Catuserbot is one of the popular bot",
    },
)
async def _(event):
    "To translate the text."
    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str or "en"
    elif ";" in input_str:
        lan, text = input_str.split(";")
    else:
        return await edit_delete(
            event, "** قم بالرد على الرسالة للترجمة **", time=5
        )
    await event.reply(text)
    text = soft_deEmojify(text.strip())
    lan = lan.strip()
    await event.reply(str(text))
    await event.reply(str(len(text)))
    if len(text) < 2:
        return await edit_delete(event, "قم بكتابة ما تريد ترجمته!")
    try:
        trans = await gtrans(text, lan)
        if not trans:
            return await edit_delete(event, "**تحقق من رمز اللغة !, لا يوجد هكذا لغة**")      
        output_str = f"**تمت الترجمة من {trans[1]} الى {lan}**\
                \n`{trans[0]}`"
        await edit_or_reply(event, output_str)
    except Exception as exc:
        await edit_delete(event, f"**خطا:**\n`{exc}`", time=5)
