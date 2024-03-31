import discord
from discord.ext import commands
import requests

def check_website_status(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx status codes)
        return f"The website <{url}> is up. Status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"The website <{url}> is down. Error: {e}"

class dadbg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.rulers = bot.rulers

    @commands.slash_command(name="dbg", description="Debug console for the bot, ignore unless you are a developer")
    async def dbgcmdy(self, ctx, commandy: discord.Option(str, name="command", description="The command you want to run"), arg1: discord.Option(str, name="arg", description="The argument for the command") = None): # type: ignore
        if str(ctx.author.id) in self.rulers:
            #ping command
            if commandy == "ping":
                if not arg1 == None:
                    web = arg1
                    if "http://" in web or "https://" in web:
                        pass
                    else:
                        web = "http://" + web
                    result = check_website_status(web)
                    await ctx.respond(result)
                else:
                    await ctx.respond("Please specify a website/IP to ping")
            #listguild
            elif commandy == "listguild":
                guild_info = [(guild.id, guild.name, guild.owner) for guild in self.bot.guilds]
                for guild_id, guild_name, guild_owner in guild_info:
                    embed = discord.Embed(title=guild_name, description=f"**Owner:** {guild_owner}\n**ID:** {guild_id}")
                    await ctx.respond(embed=embed, ephemeral=True)
            elif commandy == "blacklist":
                if not arg1 == None:
                    arg1 = arg1.replace("<", "").replace("@", "").replace(">", "")
                    if str(arg1) == str(self.bot.rulers[0]):
                        await ctx.respond("You can't blacklist the main ruler.")
                        return
                    else:
                        with open("blusers", "a") as blfile:
                            blfile.write(f"{arg1}\n")
                        await ctx.respond(f"Blacklisted {arg1}")
                    await ctx.respond(result)
                else:
                    await ctx.respond("Please specify a user to blacklist")
            elif commandy == "unblacklist":
                if arg1 is not None:
                    arg1 = arg1.replace("<", "").replace("@", "").replace(">", "")
                    with open("blusers", "r") as blfile:
                        blacklisted_users = blfile.readlines()
                    if arg1 + "\n" in blacklisted_users:
                        blacklisted_users.remove(arg1 + "\n")
                        with open("blusers", "w") as blfile:
                            blfile.writelines(blacklisted_users)
                        await ctx.respond(f"User {arg1} has been unblacklisted.")
                    else:
                        await ctx.respond(f"User {arg1} is not blacklisted.")
                else:
                    await ctx.respond("Please specify a user to unblacklist.")
            else:
                await ctx.respond("Command not found.")
            
            
        else:
            await ctx.respond("Sorry, you don't have permission to run this command.", ephemeral=True)

def setup(bot):
    bot.add_cog(dadbg(bot))