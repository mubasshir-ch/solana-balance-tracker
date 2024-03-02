import logging
import discord
from discord.ext import commands, tasks

from .tracker_api import TrackerAPI

class TrackerCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.api = TrackerAPI(self.bot.WALLET_ADDRESS, self.bot.TOKEN_MINT_ADDRESS)
        self.track_balance.start()

    def cog_unload(self):
        self.track_balance.cancel()    

    @tasks.loop(seconds=60)
    async def track_balance(self):
        await self.bot.wait_until_ready()

        try:
            guild = await self.bot.fetch_guild(int(self.bot.GUILD_ID))
            channel = await guild.fetch_channel(int(self.bot.CHANNEL_ID))
            balance = self.api.get_balance()
            # APEPOT-4-USDC
            await channel.edit(name=f"APEPOT-{balance}-USDC")

        except Exception as e:
            logging.error(f"Failed to get balance: {e}")
    


def setup(bot:commands.Bot):
    bot.add_cog(TrackerCog(bot))