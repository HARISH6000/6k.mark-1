import discord
import os
import requests
import json
import random
from replit import db
from AnilistPython import Anilist
from keep_alive import keep_alive

anilist = Anilist()

sad_emojis = [":smiling_face_with_tear:", ":slight_smile:", ":disappointed:",
":pensive:", ":worried:", ":confused:", ":slight_frown:", ":frowning2:",
":persevere:", ":confounded:", ":tired_face:", ":weary:", ":cry:", ":sob:",
":disappointed_relieved:"]

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
    try:
      x = msg.content.split("6k qa ",1)[1]
      aqua = get_animequotea(x)
      await msg.channel.send(aqua)
    except:
      await msg.channel.send(f"Anime not found {sad_emojis[random.randrange(0,14)]}")

  if msg.content.startswith('6k qc'):
    try:
      x = msg.content.split("6k qc ",1)[1]
      aquc = get_animequotec(x)
      await msg.channel.send(aquc)

    except:
      await msg.channel.send(f"Character not found {sad_emojis[random.randrange(0,14)]}")

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

  if msg.content.startswith('6k anime '):
    x = msg.content.split("6k anime ",1)[1]
    data = anilist.getAnimeInfo(x)
    n = data['name_romaji']
    await msg.channel.send(n)
    l = len(data['genres'])
    gl=data['genres']
    g=""
    for x in range(l):
      g = g+gl[x]
      if (l-1)>0:
        g=g+", "
        l=l-1
    ani = discord.Embed(title = n,description = data['desc'], color = discord.Colour.blue())
    ani.set_thumbnail(url = f"{data['cover_image']}")
    ani.add_field(name = 'Average score',value = data['average_score'],inline= False)
    ani.add_field(name = 'Genre',value = g,inline= False)
    if str(data['banner_image']) != "None":
      ani.set_image(url = f"{data['banner_image']}")

    await msg.channel.send(embed = ani)
    #except:
      #await msg.channel.send(f"Anime info not found {sad_emojis[random.randrange(0,14)]}")

  if msg.content.startswith("6k help"):
    user_name = str(msg.author).split('#')[0]
    help = discord.Embed(
      title = "Avaliable Commands",
      descripion = "Comming soon...",
      color = discord.Colour.blue()
      )
    help.set_author(name =f"{user_name}", icon_url=msg.author.avatar_url)
    #help.set_thumbnail(url = 'https://c4.wallpaperflare.com/wallpaper/320/607/818/anime-naruto-kakashi-hatake-naruto-uzumaki-wallpaper-preview.jpg')
    help.add_field(name= 'Anime Quotes', value ='1. 6k aq(gives a random anime quote) \n2.6k qa <anime name> \n3.6k qc <Character name>', inline=False)
    help.add_field(name= 'Quotes', value ='1. 6k Q (gives a random quote)', inline=False)
    help.add_field(name= 'Encouraging Messages', value ='1. 6k enc respond true (Turns on the encouraging reply)\n2. 6k enc respond false (Turns off the encouraging reply)\n3. 6k enc list (Gives the list of encouraging replies given by the users)\n4. 6k new enc <Here goes ur enc msg>(to add new replies)\n5. 6k del enc <Here goes ur enc msg> (to delete the existing reply)', inline=True)
    

    await msg.channel.send(embed = help)




keep_alive()
client.run(my_secret)


# aq gives random anime quote
# qa gives the requested anime quote
# Q gives the quote by real people
# qc is quote by character 
