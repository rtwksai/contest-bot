#!/usr/bin/python3
import discord
import traceback
from discord.ext import commands
from discord.ext.commands import errors

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """
        The event triggered when an the bot is ready to be used
        """
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game('with Codes'))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        """
        The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context(message)
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """
        if isinstance(err, errors.MissingRequiredArgument) or isinstance(err, errors.BadArgument):
            helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
            await ctx.send_help(helper)

        elif isinstance(err, errors.CommandInvokeError):
            error = traceback(err.original)
            if "2000 or fewer" in str(err) and len(ctx.message.clean_content) > 1900:
                return await ctx.send(
                    "{message.author.mention} You attempted to make the command display more than 2,000 characters...\n"
                    "Both error and command will be ignored."
                )

            await ctx.send(f"{ctx.author.mention}\nThere was an error processing the command ;-;\n{error}")

        elif isinstance(err, errors.CheckFailure):
            pass

        elif isinstance(err, errors.MaxConcurrencyReached):
            await ctx.send("{ctx.author.mention}\nYou've reached max capacity of command usage at once, please finish the previous one...")

        elif isinstance(err, errors.CommandOnCooldown):
            await ctx.send(f"{ctx.author}.mention\n This command is on cooldown... try again in {err.retry_after:.2f} seconds.")

        elif isinstance(err, errors.CommandNotFound):
            await ctx.send(f"{ctx.author.mention}\nThe command that you tried doesn't exist.\nDo check out `-help` for more info on commands")
            pass

def setup(bot):
    bot.add_cog(Events(bot))