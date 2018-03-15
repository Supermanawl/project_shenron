from discord import Game
from discord.ext.commands import Bot
import asyncio
import random
import toolkit
import game_library
import restaurants
import shenron_config


BOT_PREFIX = ("!", "?")
bot = Bot(command_prefix=BOT_PREFIX)
TOKEN = "NDE4OTMyNzAyNDExMjI3MTQ3.DXoxDQ.br6DwIJpUgdmEUJb-pe_ffcPK0A"

exp = 0
dragon_balls_collected = 0


@bot.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(bot.user.name))
    print("ID: {}".format(bot.user.id))
    await bot.change_presence(game=Game(name=random.choice(game_library.games)))


@bot.command(pass_context=True)
async def fight(ctx, name):
    global exp
    global dragon_balls_collected

    if bool(random.getrandbits(1)) and dragon_balls_collected < 7:
        await bot.send_typing(ctx.message.channel)
        await asyncio.sleep(1)
        exp += 100
        await bot.say('You have defeated ' + name + '!')
        await bot.say('Exp: ' + str(exp))
        dragon_balls_collected += 1
        await bot.say('DragonBalls: ' + str(dragon_balls_collected))
    elif dragon_balls_collected == 7:
        await bot.send_typing(ctx.message.channel)
        await asyncio.sleep(1)
        await bot.say('You have acquired enough dragon balls to summon me...')
    else:
        await bot.send_typing(ctx.message.channel)
        await asyncio.sleep(1)
        await bot.say('You have lost to ' + name + '!')
        await bot.say('Exp: ' + str(exp))
        await bot.say('DragonBalls: ' + str(dragon_balls_collected))


@bot.command(pass_context=True)
async def food(ctx):
    await bot.send_typing(ctx.message.channel)
    await asyncio.sleep(2)
    await bot.say('You want ' + random.choice(restaurants.ruston) + " today...")


@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    global dragon_balls_collected
    global exp

    if message.author == bot.user:
        return
    if message.content.startswith('I CALL ON THE MIGHTY SHENRON!'):
        if dragon_balls_collected == 7:
            await bot.send_typing(message.channel)
            await asyncio.sleep(4)
            await bot.send_message(message.channel, '{0.author.mention}, What is your wish? You will have only one!'
                                .format(message))
            await bot.wait_for_message(author=message.author)
            await bot.send_typing(message.channel)
            await asyncio.sleep(4)
            await bot.send_message(message.channel, 'A simple matter... very well {0.author.mention}, I shall grant your wish'
                                 .format(message))

            # This is where you will grant the wish so you'll probably need to wait a while why he fetches

            await bot.send_message(message.channel, 'The wish has been granted... farewell')
            dragon_balls_collected = 0
            exp = 0
        elif dragon_balls_collected > 7:
            await bot.send_typing(message.channel)
            await asyncio.sleep(4)
            await bot.send_message(message.channel, '...' + str(dragon_balls_collected) + '? ')
            dragon_balls_collected = 0
            exp = 0
            await bot.send_typing(message.channel)
            await asyncio.sleep(4)
            await bot.send_message(message.channel, 'Exp: ' + str(exp))
            await bot.send_message(message.channel, 'DragonBalls: ' + str(dragon_balls_collected))
        else:
            await bot.send_typing(message.channel)
            await asyncio.sleep(4)
            await bot.send_message(message.channel, 'You have not proven yourself to be worthy of my power...')

    await bot.process_commands(message)

# Run the bot
bot.run(shenron_config.token)

# CODE YOU USED TO CREATE A SERVER
# if wish.content.startswith('Create channel') or wish.content.startswith('Create channel'.lower()):
#     wish = wish.content.split()
#     if (len(wish) > 2):
#         new_channel = wish[2]
#     server = message.server
#     bot.create_channel(server, new_channel, type=discord.ChannelType.text)
