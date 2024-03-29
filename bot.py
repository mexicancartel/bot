#!/bin/python

import config

import os, telebot, yt_dlp

bot = telebot.TeleBot(config.BOT_TOKEN)

@bot.message_handler(commands=['start', 'mexicancartel'])
def welcome(message):
    bot.reply_to(message, "Wtf bro wat u want?")

@bot.message_handler(commands=['stkrElement'])
def stickerToElement(message):
    bot.send_message(message.chat.id, "Attempt started")
    print(message.text)
    head = message.text.find("addstickers/")
    if head == -1:
        bot.send_message(message.chat.id, "Send correct sticker link u idiot")
        return 0
    s = ""
    for i in range(len(message.text)-head):
        s += message.text[head+i]
    sticklink = "https://t.me/" + s
    if os.path.isfile("stickerpack.git.lock"):
        bot.reply_to(message, "Looks like another pack is currently being imported. Send link later.")
        return 0
    os.system("touch stickerpack.git.lock")
    os.system("addStickerToMatrix.sh "+sticklink)
    bot.reply_to(message, "Hopefully, "+s+" will be added to Matrix...(Soon™)")
    os.remove("stickerpack.git.lock")

@bot.message_handler(commands=['instadl'])
def instadl(message):
    bot.send_message(message.chat.id, "Attempt started")
    #os.chdir("instadl")
    os.system("yt-dlp "+ message.text.replace("/instadl ", "") + " -o instadl/insta.mp4")
    print(message.text)
    #os.chdir("..")
    bot.send_video(message.chat.id, telebot.types.InputFile("instadl/insta.mp4"))
    os.system("rm instadl/insta*")

@bot.message_handler(commands=['ytdl'])
def ytdl(message):
    bot.send_message(message.chat.id, "Attempt started")
    #os.chdir("instadl")
    ID=message.text.replace("/ytdl https://youtu.be/","")
    ID=ID.replace("/ytdl https://youtube.com/watch?v=","")
    os.system("yt-dlp "+ message.text.replace("/ytdl ", "") + " -o ytdl/"+ID)
    print(message.text)
    os.system("mv ytdl/"+ID+"* ytdl/yt.mp4")
    bot.send_video(message.chat.id, telebot.types.InputFile("ytdl/yt.mp4"), timeout=10000, supports_streaming=True)
    os.system("rm ytdl/yt.*")

@bot.message_handler(commands=['ytdlmusic'])
def ytdlmusic(message):
    bot.reply_to(message, "I'm Tryna download da aauudioooooo...🎶🎵🎼")
    URL = message.text.replace("/ytdlmusic ","")
    ID=message.text.replace("/ytdlmusic https://youtu.be/","")
    ID=ID.replace("/ytdl https://youtube.com/watch?v=","")
    info=yt_dlp.YoutubeDL().extract_info(URL, download=False)
    vid_title=info.get('title', None)
    ytdl_opts = {
        'outtmpl': 'ytdl/'+vid_title+'.m4a',
        'format': 'bestaudio'
    }
    dl = yt_dlp.YoutubeDL(ytdl_opts)
    dl.download(URL)
    bot.send_audio(message.chat.id, telebot.types.InputFile("ytdl/"+vid_title+".m4a"), timeout=10000)
    os.remove("ytdl/"+vid_title+".m4a")

@bot.message_handler(func=lambda msg: True)
def tweet_to_nit(message):
    if "x.com" in message.text: 
        bot.reply_to(message, message.text.replace("x.com","nitter.net"))
    elif "twitter.com" in message.text:
        bot.reply_to(message, message.text.replace("twitter.com","nitter.net"))

@bot.message_handler(func=lambda msg: True)
def echoing(message):
    if message.chat.id==0:          #disabled
        bot.reply_to(message, message.text)

bot.infinity_polling(timeout=1000)
