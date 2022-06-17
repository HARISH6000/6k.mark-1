import discord
import os
import requests
import json
import random
import time
from replit import db
from AnilistPython import Anilist
from keep_alive import keep_alive

anilist = Anilist()


sad_emojis = [":smiling_face_with_tear:", ":slight_smile:", ":disappointed:",
":pensive:", ":worried:", ":confused:", ":slight_frown:", ":frowning2:",
":persevere:", ":confounded:", ":tired_face:", ":weary:", ":cry:", ":sob:",
":disappointed_relieved:"]

my_secret = os.environ['Token']
my_id = os.environ['id']
invite_link= os.environ['invlink']
client = discord.Client()

db["filter"] = True

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

def charlist(x):
  max_result = 0
  counter = 0
  list=""
  data = anilist.extractID.character(x)
  for i in range(len(data['data']['Page']['characters'])):
    first_name = data['data']['Page']['characters'][i]['name']['first']
    last_name = data['data']['Page']['characters'][i]['name']['last']
    max_result = i + 1
    if last_name == None:
      print(f"{counter + 1}. {first_name}")
      list=list+f"{counter + 1}. {first_name}"+"\n"
    elif first_name == None:
      print(f"{counter + 1}. {last_name}")
      list = list+f"{counter + 1}. {last_name}"+"\n"
    else:
      print(f'{counter + 1}. {last_name}, {first_name}')
      list = list+f'{counter + 1}. {last_name}, {first_name}'+"\n"
    counter += 1
  if counter>1:
    list = list +"Please select the character that you are searching for in number:"
    return list
  elif counter==0:
    return "Can't find the character"
  else:
    return list


def charid(character_name,input):
  max_result = 0
  counter = 0
  data = anilist.extractID.character(character_name)
  for i in range(len(data['data']['Page']['characters'])):
    first_name = data['data']['Page']['characters'][i]['name']['first']
    last_name = data['data']['Page']['characters'][i]['name']['last']
    max_result = i + 1
    if last_name == None:
      print(f"{counter + 1}. {first_name}")
    elif first_name == None:
      print(f"{counter + 1}. {last_name}")
    else:
      print(f'{counter + 1}. {last_name}, {first_name}')
    counter += 1
  if counter > 1:
    try:
      user_input = input
      print(user_input)
    except TypeError:
      print(f"Your input is incorrect! Please try again!")
      return -1
    if user_input > max_result or user_input <= 0:
      print("Your input does not correspound to any of the characters!")
      return -1
    elif counter == 0:
      print(f'No search result has been found for the character "{character_name}"!')
      return -1
  else:
    user_input=1
  return data['data']['Page']['characters'][user_input - 1]['id']
def getCharacterInfo(cid):
  character_id = cid
  if character_id == -1:
    return None

  data = anilist.extractInfo.character(character_id)
  character_lvl = data['data']['Character']

  first_name = character_lvl['name']['first']
  last_name = character_lvl['name']['last']
  native_name = character_lvl['name']['native']

  desc = character_lvl['description']
  image = character_lvl['image']['large']

  character_dict = {"first_name": first_name,
                    "last_name": last_name,
                    "native_name": native_name,
                    "desc": desc,
                    "image": image,}

  return character_dict

def mangalist(x):
  data= anilist.extractID.manga(x)
  max_result=0
  counter=0
  list=""
  for i in range(len(data['data']['Page']['media'])):
    curr_manga=data['data']['Page']['media'][i]['title']['romaji']
    list = list+f"{counter+1}.{curr_manga}"+"\n"
    counter+=1
  list=list+"Select the number coresponding to your manga"
  return list

def MangaId(x,n):
  data= anilist.extractID.manga(x)
  max_result=0
  counter=0
  list=""
  for i in range(len(data['data']['Page']['media'])):
    curr_manga=data['data']['Page']['media'][i]['title']['romaji']
    list = list+f"{counter+1}.{curr_manga}"+"\n"
    counter+=1
    max_result+=1
  print(list)
  if counter > 1:
    try:
      user_input = n
    except TypeError:
      print(f"Your input is incorrect! Please try again!")
      return -1

    if user_input > max_result or user_input <= 0:
      MangaId.uinv="Your input does not correspound to any of the anime displayed!"
      print("Your input does not correspound to any of the anime displayed!")
      return -1
  elif counter == 0:
    print(f'No search result has been found for the anime "{x}"!')
    return -1
  else:
    user_input = 1
  print(data['data']['Page']['media'][user_input - 1]['id'])
  return data['data']['Page']['media'][user_input - 1]['id']
def MangaInfo(mid):
  if mid == -1:
    return None

  data = anilist.extractInfo.manga(mid)
  print(data)
  media_lvl = data['data']['Media']
  
  romaji = media_lvl['title']['romaji']
  eng= media_lvl['title']['english']
  desc = media_lvl['description']
  cov_img = media_lvl['coverImage']['large']
  ban_img = media_lvl['bannerImage']
  form = media_lvl['format']
  chap = media_lvl['chapters']
  vol = media_lvl['volumes']
  status =  media_lvl['status']
  start_year = media_lvl['startDate']['year']
  start_month = media_lvl['startDate']['month']
  start_day = media_lvl['startDate']['day']
  end_year = media_lvl['endDate']['year']
  end_month = media_lvl['endDate']['month']
  end_day = media_lvl['endDate']['day']
  starting_time = f'{start_day}/{start_month}/{start_year}'
  ending_time = f'{end_day}/{end_month}/{end_year}'
  #next_airing_ep = media_lvl['nextAiringEpisode']
  avg_score =  media_lvl['averageScore']
  mean_score =  media_lvl['meanScore']
  geners = media_lvl['genres']
  synonyms = media_lvl['synonyms']

  gen=""
  l=len(geners)
  for i in range(len(geners)):
    gen=gen+geners[i]
    if (l-1)>0:
      gen=gen+", "
      l=l-1
  
  syn=""
  l=len(synonyms)
  for i in range(l):
    syn=syn+synonyms[i]
    if (l-1)>0:
      syn=syn+", "
      l=l-1

  manga_dict = {
    "romaji":romaji,
    "eng":eng,
    "desc":desc,
    "cov":cov_img,
    "ban":ban_img,
    "form":form,
    "chap":chap,
    "vol":vol,
    "status":status,
    "start":starting_time,
    "end":ending_time,
    "avg":avg_score,
    "mean":mean_score,
    "geners":gen,
    "syn":syn,
  }

  return manga_dict

  
def simanimelist(x):
  data = anilist.extractID.anime(x)
  max_result = 0
  counter = 0
  list = ""
  for i in range(len(data['data']['Page']['media'])):
    curr_anime = data['data']['Page']['media'][i]['title']['romaji']
    list = list + f"{counter + 1}. {curr_anime}"+"\n" 
    max_result = i + 1
    counter += 1
  listg = list+"Select the number conresponding to your anime"
  return listg

def intcheck(message):
    try:
        int(message.content)
        return True
    except ValueError:
        return False
def string(x,n):
  s=""
  if n>4096:
    i=0
    while i < 4000:
      if x[i]=="<" and x[i+1] =="b" and x[i+2] =="r" and x[i+3] ==">" and x[i+4] =="\n":
        i=i+4
        s=s
        continue
      if x[i]=="<" and x[i+1] =="a" and x[i+2] ==" " and x[i+3] =="h" and x[i+4] =="r" and x[i+5] =="e" and x[i+6] =="f":
        s=s+"( [Read at Anilist]("
        i=i+9
      else:
        s=s+x[i]
        i=i+1
    s=s.replace("<br>", "\n")
    s=s.replace("<b>", "**")
    s=s.replace("</b>", "**")
    s=s.replace("</i>", "*")
    s=s.replace("<i>", "*")
    s=s.replace("__","**")
    s=s.replace("~!","||")
    s=s.replace("!~","||")
    s=s.replace('">',") ) ")
    s=s.replace("</a>"," ")

    return s
  else:
    i=0
    while i < n:
      if x[i]=="<" and x[i+1] =="b" and x[i+2] =="r" and x[i+3] ==">" and x[i+4] =="\n":
        i=i+4
        s=s
        continue
      if x[i]=="<" and x[i+1] =="a" and x[i+2] ==" " and x[i+3] =="h" and x[i+4] =="r" and x[i+5] =="e" and x[i+6] =="f":
        s=s+"( [Read at Anilist]("
        i=i+9
        continue
      else:
        s=s+x[i]
        i=i+1
    s=s.replace("<br>", "\n")
    s=s.replace("__","**")
    s=s.replace("<b>", "**")
    s=s.replace("</b>", "**")
    s=s.replace("</i>", "*")
    s=s.replace("<i>", "*")
    s=s.replace("~!","||")
    s=s.replace("!~","||")
    s=s.replace('">',") ) ")
    s=s.replace("</a>"," ")
    return s

@client.event
async def on_ready():
  print('We are in as {0.user}'.format(client))
  await client.change_presence(status=discord.Status.online, activity=discord.Game('6k help'))


@client.event
async def on_message(msg):
  if msg.author == client.user:
    return
# some basic commands
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
      index = int(msg.content.split("6k del enc ",1)[1])-1
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
      
#6k help
      
  if msg.content.startswith("6k help"):
    user_name = str(msg.author).split('#')[0]
    help = discord.Embed(
      title = "Avaliable Commands",
      descripion = "Comming soon...",
      color = discord.Colour.blue()
      )
    help.set_author(name =f"{user_name}", icon_url=msg.author.avatar_url)
    #help.set_thumbnail(url = 'https://c4.wallpaperflare.com/wallpaper/320/607/818/anime-naruto-kakashi-hatake-naruto-uzumaki-wallpaper-preview.jpg')
    help.add_field(name= 'Info', value ='1. 6k anime <here goes the name>\n2.6k char <here goes the name>\n3.6k manga <here goes the name>', inline=False)
    help.add_field(name= 'Anime Quotes', value ='1. 6k aq(gives a random anime quote) \n2.6k qa <anime name> \n3.6k qc <Character name>', inline=False)
    help.add_field(name= 'Quotes', value ='1. 6k Q (gives a random quote)', inline=False)
    help.add_field(name= 'Encouraging Messages', value ='1. 6k enc respond true (Turns on the encouraging reply)\n2. 6k enc respond false (Turns off the encouraging reply)\n3. 6k enc list (Gives the list of encouraging replies given by the users)\n4. 6k new enc <Here goes ur enc msg>(to add new replies)\n5. 6k del enc <Here goes the number coresponding to the enc msg> (to delete the existing reply)', inline=True)
    

    await msg.channel.send(embed = help)
   #Info commands
  if msg.content.startswith("6k filter "):
    bo = msg.content.split("6k filter ",1)[1]
    if bo.lower()=="true":
      db["filter"] = True
      await msg.channel.send("Filter is turned on.")
    if bo.lower()=="false":
      db["filter"] = False
      await msg.channel.send("Filter is turned off.")
  def AnimeId(x,input):
    data = anilist.extractID.anime(x)
    max_result = 0
    counter = 0
    list = ""
    for i in range(len(data['data']['Page']['media'])):
      curr_anime = data['data']['Page']['media'][i]['title']['romaji']
      list = list + f"{counter + 1}. {curr_anime}"+"\n" 
      max_result = i + 1
      counter += 1

    print(list)
    if counter > 1:
      try:
        user_input = input
      except TypeError:
        print(f"Your input is incorrect! Please try again!")
        return -1

      if user_input > max_result or user_input <= 0:
        AnimeId.uinv="Your input does not correspound to any of the anime displayed!"
        print("Your input does not correspound to any of the anime displayed!")
        return -1
    elif counter == 0:
      print(f'No search result has been found for the anime "{x}"!')
      return -1
    else:
      user_input = 1
    print(data['data']['Page']['media'][user_input - 1]['id'])
    return data['data']['Page']['media'][user_input - 1]['id']

  def AnimeInfo(aid):
    if aid == -1:
      return None
    data = anilist.extractInfo.anime(aid)
    media_lvl = data['data']['Media']
    #studio=media_lvl['studio']
    episodes=media_lvl['episodes']
    name_romaji = media_lvl['title']['romaji']
    name_english = media_lvl['title']['english']
    start_year = media_lvl['startDate']['year']
    start_month = media_lvl['startDate']['month']
    start_day = media_lvl['startDate']['day']
    end_year = media_lvl['endDate']['year']
    end_month = media_lvl['endDate']['month']
    end_day = media_lvl['endDate']['day']
    starting_time = f'{start_day}/{start_month}/{start_year}'
    ending_time = f'{end_day}/{end_month}/{end_year}'
    next_airing_ep = media_lvl['nextAiringEpisode']
    cover_image = media_lvl['coverImage']['large']
    banner_image = media_lvl['bannerImage']
    airing_format = media_lvl['format']
    airing_status = media_lvl['status']
    airing_episodes = media_lvl['episodes']
    season = media_lvl['season']
    desc = media_lvl['description']
    average_score = media_lvl['averageScore']
    genres = media_lvl['genres']

    anime_dict = {
      "name_romaji": name_romaji,
      #"studios":studios,
      "episodes":episodes,
      "name_english": name_english,
      "starting_time": starting_time,
      "ending_time": ending_time,
      "cover_image": cover_image,
      "banner_image": banner_image,
      "airing_format": airing_format,
      "airing_status": airing_status,
      "airing_episodes": airing_episodes,
      "season": season,
      "desc": desc,
      "average_score": average_score,
      "genres": genres,
      "next_airing_ep": next_airing_ep,
     }
    return anime_dict
  if msg.content.startswith('6k anime '):
    x = msg.content.split("6k anime ",1)[1]
    await msg.channel.send(simanimelist(x))
    message = await client.wait_for("message",check=intcheck, timeout=60)
    input=int(message.content)
    print(input)
    aid = AnimeId(x,input)
    isAdult=(anilist.extractID.anime(x)['data']['Page']['media'][input - 1]['isAdult'])
    print(isAdult)
    if db["filter"] and str(isAdult) == "True":
      await msg.channel.send("Nsfw filter is turned on. Use ||6k filter false|| command to turn off the filter. ")
    else:
      data = AnimeInfo(aid)
      n = data['name_romaji']
      l = len(data['genres'])
      gl=data['genres']
      g=""
      for x in range(l):
        g = g+gl[x]
        if (l-1)>0:
          g=g+", "
          l=l-1
      boo = False
      if str(data['banner_image']) =="None":
        boo = True
      #date = data['next_airing_ep']['airingAt']
      print(anilist.extractInfo.anime(aid))
      des=string(data['desc'],len(data['desc']))
      ani = discord.Embed(title = n,description = des, color = discord.Colour.blue())
      if str(data['banner_image']) =="None":
        ani.set_image(url = f"{data['cover_image']}")
      ani.add_field(name = 'Genre',value = g,inline= boo)
      ani.add_field(name = 'Status',value = data['airing_status'],inline= boo)
      if str(data['episodes']) != "None":
        ani.add_field(name = 'Episodes',value = data['episodes'],inline= boo)
      #if str(data['studio']) != "None":
        #ani.add_field(name = 'Studio',value = data['studio'],inline= boo)
      ani.add_field(name = 'Format',value = data['airing_format'],inline= boo)
      ani.add_field(name = 'Started at',value = data['starting_time'],inline= boo)
      if str(data['ending_time']) != "None/None/None":
        ani.add_field(name = 'Ended at',value=data['ending_time'],inline=boo)
      if str(data['next_airing_ep']) != "None":
        tleft = str(data['next_airing_ep']['timeUntilAiring']/(60*60*24))+" days"
        ani.add_field(name = 'Next Episode',value=data['next_airing_ep']['episode'],inline=boo)
        ani.add_field(name = 'Time left for Next Episode',value=tleft,inline=boo)
      ani.add_field(name = 'Average score',value = data['average_score'],inline= boo)
      if str(data['banner_image']) != "None":
        ani.set_thumbnail(url = f"{data['cover_image']}")
        ani.set_image(url = f"{data['banner_image']}")
    
      await msg.channel.send(embed = ani)
    #except:
      #await msg.channel.send(f"Anime info not found {sad_emojis[random.randrange(0,14)]}")

  if msg.content.startswith("6k char "):
    x = msg.content.split("6k char ",1)[1]
    await msg.channel.send("**CONTAINS SPOILERS FOR BOTH ANIME AND MANGA SO PROCEED WITH CAUTION**")
    await msg.channel.send(charlist(x))
    choice = await client.wait_for("message",check=intcheck, timeout=60)
    input=int(choice.content)
    print(input)
    cid=charid(x,input)
    info=anilist.extractInfo.character(cid)
    print(cid)
    print(info)
    data=getCharacterInfo(cid)
    if data['first_name'] and data['last_name'] != None:
      n=data['first_name']+" "+data['last_name']
    else:
      n=data['first_name']
    if(str(data['desc'])) != "None":
      des=string(data['desc'],len(data['desc']))
      if len(data['desc'])>4096:
        des = des+"..... "+"[Read more](https://anilist.co/character/"+str(cid)+"/)"
        ani = discord.Embed(title =n,description = des, color = discord.Colour.blue())
      else:
        ani = discord.Embed(title =n,description = des, color = discord.Colour.blue())
    else:
      ani = discord.Embed(title =n,description = "Description is not available for this character.", color = discord.Colour.blue())
    if(str(data['image'])) != "None":
      ani = ani.set_thumbnail(url = f"{data['image']}")
    
    await msg.channel.send(embed = ani)
  
  if msg.content.startswith("6k manga "):
    x = msg.content.split("6k manga ",1)[1]
    await msg.channel.send(mangalist(x))
    message = await client.wait_for("message",check=intcheck, timeout=60)
    input=int(message.content)
    print(input)
    mid = MangaId(x,input)
    data = MangaInfo(mid)
    des=string(data['desc'],len(data['desc']))

    man = discord.Embed(title=data['romaji'],description=des,color = discord.Colour.blue())
    if(str(data['cov']))!="None":
      man.set_thumbnail(url = f"{data['cov']}")
    if(str(data['ban'])) != "None":
      man.set_image(url = f"{data['ban']}")
    man.add_field(name = 'Other names',value =data['syn'],inline=False)
    man.add_field(name = 'Genre',value =data['geners'],inline= False)
    man.add_field(name = 'Status',value = data['status'],inline=False)
    if str(data['chap']) != "None":
      man.add_field(name = "Chapters",value = data['chap'],inline=False)
    if str(data['vol']) != "None":
      man.add_field(name = "Volume",value = data['vol'],inline=False)
    if data['start'] != "None/None/None":
      man.add_field(name = "Started at",value = data['start'],inline=False)
    if data['end'] != "None/None/None":
      man.add_field(name = "Ended at",value = data['end'],inline=False)
    if data['avg'] != "None":
      man.add_field(name = "Average Score",value =data['avg'],inline=False)
    if data['mean'] != "None":
      man.add_field(name = "Mean Score",value = data['mean'],inline =False)

    await msg.channel.send(embed = man)
  
# commands and features for devs

  if msg.content.startswith("6k server count"):
    if str(msg.author.id) == f"{my_id}":
      server_names = list(client.guilds)
      n=0
      user_name = str(msg.author).split('#')[0]
      names =""
      for guild in client.guilds:
        n = n + 1
        names += f"{n}.{guild.name}" + "\n"
      sc = discord.Embed(title="Server Count",description=f"I am monitoring {len(server_names)} servers",color = discord.Colour.blue())
      sc.add_field(name="Servers", value=names, inline=False)
      sc.add_field(name="Latency",value=(f'Pong! In {round(client.latency * 1000)}ms'))
      sc.set_author(name=f"{user_name}",icon_url=msg.author.avatar_url)
      await msg.channel.send(embed=sc)
    else:
      await msg.channel.send("Sry,You are not authorised to use this command.")
    
  if str(msg.channel.type) == 'private':
    dm = discord.utils.get(client.get_all_channels(), guild__name='H6k\'s bots', name='6k-dm')

    if msg.attachments != []:
      files= msg.attachments
      for file in files:
        await dm.send("["+msg.author.display_name+"] ")
        await dm.send(file.url)
    else:
      await dm.send("["+msg.author.display_name+"] "+msg.content)
  if str(msg.channel) == '6k-dm' and msg.content.startswith("<") and str(msg.author.id) == f"{my_id}":
    mention=msg.mentions[0]
    if msg.attachments != []:
      files= msg.attachments
      for file in files:
        await mention.send(file.url)
    else:
      index = msg.content.index(" ")
      seithi=msg.content[index:]
      await mention.send(seithi)



# some anime reference for fun
  if msg.content.startswith("give me notes"):
    await msg.channel.send("Ask your friends bruh... oh... I see, you don't have any")
  if msg.content.startswith("where is sniper island"):
    us= discord.Embed(title="It's in your heart",color = discord.Colour.from_rgb(165, 42, 42))
    us.set_author(name="Sogeking",icon_url="https://preview.redd.it/9m4294s8wpz41.jpg?auto=webp&s=94fd1b1ddebfb38c09562163e9ba8d3f4e01bf4f")
    us.set_thumbnail(url = "https://static.wikia.nocookie.net/onepiece/images/3/38/Sogeking.jpeg/revision/latest/top-crop/width/360/height/450?cb=20110203170225&path-prefix=pt")

    await msg.channel.send("It's in our hearts")
  

keep_alive()
client.run(my_secret)


# aq gives random anime quote
# qa gives the requested anime quote
# Q gives the quote by real people
# qc is quote by character 
