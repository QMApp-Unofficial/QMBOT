    @commands.hybrid_command(name="confess", description="Send an anonymous confession.")
    async def confess(self, ctx, *, confession: str):
        CONFESSIONS_CHANNEL_ID = 1492170739955138630
        LOG_USER_ID = 734468552903360594

        try:
            await ctx.message.delete()
        except Exception:
            pass

        if not ctx.guild:
            return await ctx.send(
                embed=error("Confession", "This command can only be used in a server."),
                ephemeral=True
            )

        confessions_channel = ctx.guild.get_channel(CONFESSIONS_CHANNEL_ID)
        if confessions_channel is None:
            try:
                confessions_channel = await self.bot.fetch_channel(CONFESSIONS_CHANNEL_ID)
            except Exception:
                return await ctx.send(
                    embed=error("Confession", "Confessions channel not found."),
                    ephemeral=True
                )

        # Public anonymous confession
        public_e = embed(
            "🤫  Anonymous Confession",
            confession,
            C.NEUTRAL,
            footer="Submitted anonymously"
        )

        try:
            await confessions_channel.send(embed=public_e)
        except Exception:
            return await ctx.send(
                embed=error("Confession", "I couldn't post to the confessions channel."),
                ephemeral=True
            )

        # DM confirmation to sender
        try:
            await ctx.author.send(
                embed=embed(
                    "✅  Confession Sent",
                    f"Your confession was posted anonymously in {confessions_channel.mention}.",
                    C.WIN
                )
            )
        except Exception:
            pass

        # DM log to specified user
        log_user = self.bot.get_user(LOG_USER_ID)
        if log_user is None:
            try:
                log_user = await self.bot.fetch_user(LOG_USER_ID)
            except Exception:
                log_user = None

        if log_user is not None:
            log_embed = embed(
                "🔍  Confession Log",
                f"**Confession:**\n{confession}\n\n"
                f"**Sender:** {ctx.author.mention} (`{ctx.author}` · ID `{ctx.author.id}`)\n"
                f"**Guild:** {ctx.guild.name} (`{ctx.guild.id}`)\n"
                f"**Used In:** {ctx.channel.mention} (`{ctx.channel.id}`)\n"
                f"**Posted To:** <#{CONFESSIONS_CHANNEL_ID}>",
                C.WARN,
                footer="Private confession log"
            )
            try:
                await log_user.send(embed=log_embed)
            except Exception:
                pass
