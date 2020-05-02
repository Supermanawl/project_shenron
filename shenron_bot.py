from discord import Game
from discord.ext.commands import Bot
import asyncio
import random
import toolkit
import game_library
import restaurants
#import shenron_config


BOT_PREFIX = ("!", "?")
bot = Bot(command_prefix=BOT_PREFIX)
TOKEN = "NDE4OTMyNzAyNDExMjI3MTQ3.XqyYig.Bbun0ERFfJtwxFCxNYeujupCuTA"

dragon_balls_collected = 0

async def dragon_type(ctx, seconds):
	async with ctx.typing():
		await asyncio.sleep(seconds)


@bot.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(bot.user.name))
    print("ID: {}".format(bot.user.id))
    await bot.change_presence(activity=Game(name=random.choice(game_library.games)))

@bot.command(pass_context=True)
async def fight(ctx, name):
	global dragon_balls_collected
	
	if bool(random.getrandbits(1)) and dragon_balls_collected < 7:
		await dragon_type(ctx, 4)
		await ctx.send('You have defeated ' + name + '!')
		dragon_balls_collected += 1
		await ctx.send('DragonBalls: ' + str(dragon_balls_collected))
	elif dragon_balls_collected == 7:
		await dragon_type(ctx, 4)
		await ctx.send('You have acquired enough dragon balls to summon me...')
	else:
		await dragon_type(ctx, 4)
		await ctx.send('You have lost to ' + name + '!')
		await ctx.send('DragonBalls: ' + str(dragon_balls_collected))


# Run the bot
#bot.run(shenron_config.token)
bot.run(TOKEN)

