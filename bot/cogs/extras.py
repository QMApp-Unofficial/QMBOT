import discord
from discord.ext import commands
import time
import random

class Extras(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    # =========================
    # Utility
    # =========================

    @commands.hybrid_command()
    async def ping(self, ctx):
        """Check bot latency"""
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"🏓 Pong! `{latency}ms`")

    @commands.hybrid_command()
    async def uptime(self, ctx):
        """Bot uptime"""
        seconds = int(time.time() - self.start_time)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        await ctx.send(f"⏱️ Uptime: `{hours}h {minutes}m`")

    @commands.hybrid_command()
    async def botinfo(self, ctx):
        """Bot information"""
        await ctx.send(
            f"🤖 **Bot Info**\n"
            f"Servers: `{len(self.bot.guilds)}`\n"
            f"Users: `{len(self.bot.users)}`"
        )

    @commands.hybrid_command()
    async def serverinfo(self, ctx):
        """Server information"""
        guild = ctx.guild
        await ctx.send(
            f"🏠 **Server Info**\n"
            f"Name: `{guild.name}`\n"
            f"Members: `{guild.member_count}`\n"
            f"Created: `{guild.created_at.date()}`"
        )

    @commands.hybrid_command()
    async def userinfo(self, ctx, member: discord.Member = None):
        """User information"""
        member = member or ctx.author
        await ctx.send(
            f"👤 **User Info**\n"
            f"Name: `{member}`\n"
            f"Joined: `{member.joined_at.date() if member.joined_at else 'Unknown'}`"
        )

    @commands.hybrid_command()
    async def gif(self, ctx, *, query: str):
        """Random GIF (simple placeholder)"""
        gifs = [
            "https://media.giphy.com/media/ICOgUNjpvO0PC/giphy.gif",
            "https://media.giphy.com/media/l0HlQ7LRalQqdWfao/giphy.gif",
            "https://media.giphy.com/media/3o7aD2saalBwwftBIY/giphy.gif",
        ]
        await ctx.send(random.choice(gifs))

    @commands.hybrid_command()
    async def messagecount(self, ctx):
        """Counts messages in channel (recent only)"""
        count = 0
        async for _ in ctx.channel.history(limit=100):
            count += 1
        await ctx.send(f"💬 Last 100 messages counted: `{count}`")

    @commands.hybrid_command()
    async def timer(self, ctx, seconds: int):
        """Simple timer"""
        if seconds > 300:
            return await ctx.send("⛔ Max timer is 300 seconds.")

        await ctx.send(f"⏳ Timer started for `{seconds}` seconds...")
        await discord.utils.sleep_until(
            discord.utils.utcnow() + discord.timedelta(seconds=seconds)
        )
        await ctx.send(f"⏰ {ctx.author.mention} Timer finished!")

# =========================
# Setup
# =========================

async def setup(bot):
    await bot.add_cog(Extras(bot))
