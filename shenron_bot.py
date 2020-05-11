# Pip Install Imports
from discord import Game
from discord.ext.commands import Bot
import asyncio
import random
import logging

# Local Imports
import game_library
import rival_library
import shenron_config

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

# Command Prefixes
BOT_PREFIX = ("!", "?")
bot = Bot(command_prefix=BOT_PREFIX)

dragon_balls_collected = 0

# Show Shenron typing...
async def dragon_type(ctx, seconds):
	async with ctx.typing():
		await asyncio.sleep(seconds)


# Print bot info to console
@bot.event
async def on_ready():
    logging.info("Bot Online!")
    logging.info("Name: {}".format(bot.user.name))
    logging.info("ID: {}".format(bot.user.id))
    await bot.change_presence(activity=Game(name=random.choice(game_library.games)))


# Fight whoever you'd like for a chance at a dragonball
@bot.command(pass_context=True)
async def fight(ctx, name=None):
	global dragon_balls_collected
	participant = str(ctx.author)
	if name == None:
		name = random.choice(rival_library.rivals)

	logging.info("Fight requested by " + participant)

	if dragon_balls_collected > 7:
		await dragon_type(ctx, 1)
		await ctx.send('Do you think me a fool?')
		await dragon_type(ctx, 2)
		await ctx.send('The DragonBalls you have "collected" will now be dispersed')
		logging.info("Guild has more than 7 DragonBalls. Resetting count to 0")
		dragon_balls_collected = 0
	elif bool(random.getrandbits(1)) and dragon_balls_collected < 7:
		await dragon_type(ctx, 1)
		await ctx.send('You have defeated ' + name + '!')
		dragon_balls_collected += 1
		logging.info(participant + " won fight with " + name)
	elif dragon_balls_collected == 7:
		await dragon_type(ctx, 1)
		await ctx.send('You have acquired enough dragon balls to summon me...')
		logging.info("Enough dragon balls have been collected to call Shenron")
	else:
		await dragon_type(ctx, 1)
		await ctx.send('You have lost to ' + name + '!')
		logging.info(participant + " lost fight with " + name)

	await ctx.send('DragonBalls collected: ' + str(dragon_balls_collected))
	logging.info("DragonBalls collected: " + str(dragon_balls_collected))



# Respond to the call on shenron!
@bot.event
async def on_message(message):
	global dragon_balls_collected
	canGrantWish = False
	channel = message.channel
	caller = str(message.author)

	if message.author == bot.user:
		return
	if message.content.startswith('I CALL ON THE MIGHTY SHENRON!'):
		logging.info("Shenron has been summoned by " + caller)
		if dragon_balls_collected == 7:
			logging.info("Enough DragonBalls have been collected")
			while canGrantWish == False:
				await bot.process_commands(message)
				await dragon_type(channel, 2)
				await channel.send('{0.author.mention}, What is your wish? You will have only one!'.format(message))
				logging.info("Waiting for user input")
				await bot.wait_for('message')
				if bool(random.getrandbits(1)):
					await dragon_type(channel, 1)
					await channel.send("A simple matter...")
					await dragon_type(channel, 2)
					await channel.send("Your wish is granted...farewell.")
					canGrantWish = True
					logging.info("Wish has been granted")
				else:
					await dragon_type(channel, 2)
					await channel.send("I cannot grant a wish that exceeds the power of my creator.")
					await dragon_type(channel, 1)
					await channel.send("I'm beginning to grow impatient...")
					logging.info("Wish cannot be granted")
			dragon_balls_collected = 0
		elif dragon_balls_collected > 7:
			await dragon_type(channel, 2)
			await channel.send("You think me a fool?")
			await dragon_type(ctx, 2)
			await channel.send('The DragonBalls you have "collected" will now be dispersed')
			await dragon_type(channel, 1)
			await channel.send('DragonBalls: ' + str(dragon_balls_collected))
			logging.info("Guild has more than 7 DragonBalls. Resetting count to 0")
		else:
			logging.info("Not enough DragonBalls have been collected")
			await dragon_type(channel, 2)
			await channel.send("You have not proven yourself to be worthy of my power...")
	await bot.process_commands(message)



# Run the bot
bot.run(shenron_config.token)
