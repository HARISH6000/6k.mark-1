import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

my_secret = os.environ['Token']

client = discord.Client()

sad_words = ["sad", "depressed","hopeless","mournful","sed","depressing","despairing","miserable","heartbroken","sorry","despair","heartbroken"]

str_enc = ["Hang in there, buddy!","don`t worry", "Everything will be fine","This is tough, but you're tougher","Don't stress","Sending some good vibes and happy thoughts your way"]

if "responding" not in db.keys():
  db["responding"] = True



anime_quote = ["6k aq","6kaq","6k anime quote","6kanimequote","6k animequote"]

def get_animequote():
  response = requests.get("https://animechan.vercel.app/api/random")
  json_data = json.loads(response.text)
  animequote = json_data['quote']+ " -" + json_data['character']+ " from " + json_data['anime']
  return(animequote)


def get_animequotea(x):
  
  response = requests.get("https://animechan.vercel.app/api/quotes/anime?title="+x)
  json_data = json.loads(response.text)
  l = len(json_data)
  n = random.randint(0, l)
  animequotea = json_data[n]['quote']+ " -" + json_data[n]['character']+ " from " + json_data[n]['anime']
  return(animequotea)

def get_animequotec(x):
  
  response = requests.get("https://animechan.vercel.app/api/quotes/character?name="+x)
  json_data = json.loads(response.text)
  l = len(json_data)
  n = random.randint(0, l)
  animequotec = json_data[n]['quote']+ " -" + json_data[n]['character']+ " from " + json_data[n]['anime']
  return(animequotec)

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_enc(enc_msg):
  if "enc" in db.keys():
    enc = db["enc"]
    enc.append(enc_msg)
    db["enc"] = enc
  else:
    db["enc"] = [enc_msg]

def delete_enc(index):
  enc = db["enc"]
  if len(enc) > index:
    del enc[index]
    db["enc"] = enc




@client.event
async def on_ready():
  print('We are in as {0.user}'.format(client))

@client.event
async def on_message(msg):
  if msg.author == client.user:
    return

  if msg.content.startswith('6k hello'):
    await msg.channel.send('Hello there!')
  
  if msg.content.startswith('6k bye'):
    await msg.channel.send('See you soon')

  if msg.content.startswith('6k about'):
    await msg.channel.send("Yo, I am 6k.mark-1. Yh ...ik my name is weird. I was created by Harish 6000. He didn't give any purpose for me, like how he doesn't have any. I wish that he adds more commands to me so that I can interact with you all. For more info contact Harish 6000. See you!")

  if msg.content.startswith('6k qa'):
    x = msg.content.split("6k qa ",1)[1]
    aqua = get_animequotea(x)
    await msg.channel.send(aqua)

  if msg.content.startswith('6k qc'):
    x = msg.content.split("6k qc ",1)[1]
    aquc = get_animequotec(x)
    await msg.channel.send(aquc)

  if any(word in msg.content for word in anime_quote):
    aqu = get_animequote()
    await msg.channel.send(aqu)

  if msg.content.startswith('6k Q'):
    qu = get_quote()
    await msg.channel.send(qu)

  if db["responding"]:
    options = str_enc
    if "enc" in db.keys():
      options = options + db["enc"].value

    if any(word in msg.content for word in sad_words):
      l = len(options)
      n = random.randint(0,l)
      await msg.channel.send(options[n])

  if msg.content.startswith("6k new enc"):
    enc_msg = msg.content.split("6k new enc ",1)[1]
    update_enc(enc_msg)
    await msg.channel.send("Your encouraging message is added.")

  if msg.content.startswith("6k del enc"):
    enc = []
    if "enc" in db.keys():
      index = int(msg.content.split("6k del enc ",1)[1])
      delete_enc(index)
      enc = db["enc"]
    await msg.channel.send(enc)

  if msg.content.startswith("6k enc list"):
    enc =[]
    if "enc" in db.keys():
      enc = db["enc"]
    await msg.channel.send(enc)

  if msg.content.startswith("6k enc respond"):
    val = msg.content.split("6k enc respond ",1)[1]
    if val.lower() == "true":
      db["responding"] = True
      await msg.channel.send("I will respond to your sad messages with encouraging words")
    if val.lower() == "false":
      db["responding"] = False
      await msg.channel.send("Encouraging messages are turned off.")

keep_alive()
client.run(my_secret)

# aq gives random anime quote
# qa gives the requested anime quote
# Q gives the quote by real people
# qc is quote by character 
