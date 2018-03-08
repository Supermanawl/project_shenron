from discord import Game
from discord.ext.commands import Bot
import random
import shenron_config

BOT_PREFIX = "!"
bot = Bot(command_prefix=BOT_PREFIX)
TOKEN = "NDE4OTMyNzAyNDExMjI3MTQ3.DXoxDQ.br6DwIJpUgdmEUJb-pe_ffcPK0A"
games = ["on Discord Island", "NBA 2K18", "Pokémon Colosseum", "Portal 2", "Grand Theft Auto V", "Minecraft"]
exp = 0
dragon_balls_collected = 0
foes = {
    "frieza": {"points" : 100, "level": 5},
    "cell": {"points" : 100, "level": 5},
    "raditz": {"points": 10, "level" : 1},
    "majin buu": {"points" : 80, "level" : 4},
    "broly": {"points": 300, "level" : 5},
    "captain ginyu": {"points" : 50, "level" : 2}
}


def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))


@bot.command()
async def fight(name):
    global exp
    await bot.say('You will be fighting ' + name.title())
    if bool(random.getrandbits(1)):
        exp += foes[name.lower()]["points"]
        await bot.say('You have won!')
        await bot.say('Exp: ' + str(exp))
        await bot.say('DragonBalls: ' + str(dragon_balls_collected))
    else:
        await bot.say('You have lost!')
        await bot.say('Exp: ' + str(exp))
        await bot.say('DragonBalls: ' + str(dragon_balls_collected))


@bot.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(bot.user.name))
    print("ID: {}".format(bot.user.id))
    await bot.change_presence(game=Game(name="%s" % random.choice(games)))

@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    global dragon_balls_collected
    await bot.process_commands(message)

    if message.author == bot.user:
        return
    if message.content.startswith('I CALL ON THE MIGHTY SHENRON!'):
        if dragon_balls_collected == 7:
            await bot.send_message(message.channel, '{0.author.mention}, What is your wish? You will have only one!'
                                .format(message))
            await bot.wait_for_message(author=message.author)
            await bot.send_message(message.channel, 'A simple matter... very well {0.author.mention}, I shall grant your wish'
                                 .format(message))
            await bot.send_message(message.channel, 'The wish has been granted... farewell')
            dragon_balls_collected = 0
        else:
            await bot.send_message(message.channel, 'You have not proven yourself to be worthy of my power...')

# Run the bot
bot.run(shenron_config.token)

# CODE YOU USED TO CREATE A SERVER
# if wish.content.startswith('Create channel') or wish.content.startswith('Create channel'.lower()):
#     wish = wish.content.split()
#     if (len(wish) > 2):
#         new_channel = wish[2]
#     server = message.server
#     bot.create_channel(server, new_channel, type=discord.ChannelType.text)
