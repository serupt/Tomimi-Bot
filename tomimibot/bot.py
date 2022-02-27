from ast import alias
import os
import hikari
import lightbulb
from tomimibot.extensions.wordle.utils import generate_puzzle_embed, process_message_as_guess

guild_list = list(map(int, os.environ["GUILD_IDS"].split(",")))

bot = lightbulb.BotApp(
    os.environ["TOKEN"],
    default_enabled_guilds=guild_list,
    help_slash_command=True,
    intents=hikari.Intents.ALL,
)

@bot.listen()
async def starting_load_extensions(_: hikari.StartingEvent) -> None:
    bot.load_extensions("tomimibot.extensions.wordle.utils")
    bot.load_extensions("tomimibot.extensions.music.music")

@bot.listen(hikari.StartedEvent)
async def on_start(event):
    await bot.update_presence(activity=hikari.Activity(name="wordle. Use /wordle to play!"))
    
@bot.command()
@lightbulb.add_cooldown(30, 1, lightbulb.cooldowns.UserBucket)
@lightbulb.command("wordle", "play wordle!")
@lightbulb.implements(lightbulb.SlashCommand)
async def test(ctx: lightbulb.SlashContext) -> None:
    embed = generate_puzzle_embed(ctx.author)
    await ctx.respond(embed)

@bot.listen(hikari.GuildMessageCreateEvent)
async def on_message(event: hikari.GuildMessageCreateEvent) -> None:
    await process_message_as_guess(bot,event)


@bot.command()
@lightbulb.command("ping", "check latency of bot")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.SlashContext) -> None:
    await ctx.respond(f"Pong! Latency: {bot.heartbeat_latency*1000:.2f}ms")
    
@bot.command()
@lightbulb.add_checks(lightbulb.checks.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES),
                      lightbulb.checks.bot_has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.option("amount", "amount of message to delete", type=int, required=True, max_value=100)
@lightbulb.command("purge", "deletes a specified amount of messages")
@lightbulb.implements(lightbulb.SlashCommand)
async def purge(ctx: lightbulb.SlashContext) -> None:
    await bot.rest.delete_messages(ctx.channel_id, await bot.rest.fetch_messages(ctx.channel_id).limit(ctx.options.amount))
    await ctx.respond("Messages Deleted", delete_after=5)
    

def run() -> None:
    if os.name != "nt":
        import uvloop
        uvloop.install()
        
    bot.run()