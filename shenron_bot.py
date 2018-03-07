import discord
from discord.ext.commands import Bot
from discord.ext import commands
from pprint import pprint
import shenron_config

Client = discord.Client()
bot_prefix = "!"
bot = commands.Bot(command_prefix=bot_prefix)

def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))

@bot.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(bot.user.name))
    print("ID: {}".format(bot.user.id))
    #dump(bot.channel)

@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return
    if message.content.startswith('I CALL ON THE MIGHTY SHENRON!'):
        await bot.send_message(message.channel, '{0.author.mention}, What is your wish? You will have only one!'
                               .format(message))
        wish = await bot.wait_for_message(author=message.author)

        await bot.send_message(message.channel, 'A simple matter... very well {0.author.mention}, I shall grant your wish'
                               .format(message))

        if wish.content.startswith('Create channel') or wish.content.startswith('Create channel'.lower()):
            wish = wish.content.split()

            if(len(wish) > 2): 
                new_channel = wish[2]
            server = message.server
            await bot.create_channel(server, new_channel, type=discord.ChannelType.text)
        
        if wish.content.startswith('Destroy channel') or wish.content.startswith('Destroy channel'.lower()):
            wish = wish.content.split()

            if(len(wish) > 2): 
                old_channel = wish[2]
            server = message.server
            dump(message.server.id)
            await bot.delete_channel('old_channel')
            #print(message.server.id)
            #dump(message.server.id)
        await bot.send_message(message.channel, 'The wish has been granted... farewell')


bot.run(shenron_config.token)
