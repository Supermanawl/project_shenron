from discord import Game
from discord.ext.commands import Bot
import asyncio
import random
import toolkit
import game_library
import shenron_config


BOT_PREFIX = ("!", "?")
bot = Bot(command_prefix=BOT_PREFIX)

dragon_balls_collected = 7



# Show Shenron typing...
async def dragon_type(ctx, seconds):
	async with ctx.typing():
		await asyncio.sleep(seconds)



# Print bot info to console
@bot.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(bot.user.name))
    print("ID: {}".format(bot.user.id))
    await bot.change_presence(activity=Game(name=random.choice(game_library.games)))



# Fight whoever you'd like for a chance at a dragonball
@bot.command(pass_context=True)
async def fight(ctx, name):
	global dragon_balls_collected

	if bool(random.getrandbits(1)) and dragon_balls_collected < 7:
		await dragon_type(ctx, 1)
		await ctx.send('You have defeated ' + name + '!')
		dragon_balls_collected += 1
		await ctx.send('DragonBalls: ' + str(dragon_balls_collected))
	elif dragon_balls_collected == 7:
		await dragon_type(ctx, 1)
		await ctx.send('You have acquired enough dragon balls to summon me...')
	else:
		await dragon_type(ctx, 1)
		await ctx.send('You have lost to ' + name + '!')
		await ctx.send('DragonBalls: ' + str(dragon_balls_collected))



@bot.event
async def on_message(message):
	global dragon_balls_collected
	channel = message.channel

	if message.author == bot.user:
		return
	if message.content.startswith('I CALL ON THE MIGHTY SHENRON!'):
		if dragon_balls_collected == 7:
			await dragon_type(channel, 2)
			await channel.send('{0.author.mention}, What is your wish? You will have only one!'.format(message))
		else:
			await dragon_type(channel, 2)
			await channel.send("You have not proven yourself to be worthy of my power...")

	await bot.process_commands(message)

# Run the bot
bot.run(shenron_config.token)
