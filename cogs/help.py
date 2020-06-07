import datetime
import logging
import time

from discord import Embed
from discord.ext import commands
from discord.ext.commands import guild_only, CommandError

from util.config import config, author_discord, version, repository, karma, thanks_list, blacklist, reaction_emoji
from util.constants import embed_color
from util.conversion import strfdelta
from util.embedutil import add_filler_fields

log = logging.getLogger(__name__)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    # build info embed
    @guild_only()
    @commands.Cog.listener()
    async def on_message(self, message):
        # if bot mentioned and the content is in equal length
        # to the mention of user id, then it has to be an empty message
        if self.bot.user.mentioned_in(message) and len(message.content) == len('<@!{}>'.format(self.bot.user.id)):
            embed: Embed = Embed(colour=embed_color)
            embed.title = self.bot.user.name + "#" + self.bot.user.discriminator
            embed.description = 'A bot for handling karma points of non-bot guild members.'
            embed.add_field(name='Prefix', value=config['prefix'], inline=True)
            embed.add_field(name='Contributors', value=author_discord(), inline=True)
            version_field = '```fix\nVersion: {}\nDiscord.py: {}\nPython: {}```' \
                .format(version()['aura_version'], version()['discord_version'], version()['python_version'])
            embed.add_field(name='Build Info', value=version_field, inline=False)
            current_time = time.time()
            difference = int(round(current_time - self.start_time))
            uptime = datetime.timedelta(seconds=difference)
            embed.add_field(name='Uptime',
                            value=strfdelta(uptime, '{days} days, {hours} hours, {minutes} minutes, {seconds} seconds'),
                            inline=False)
            embed.add_field(name='Source', value=repository(), inline=False)
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            await self.bot.get_channel(message.channel.id).send(embed=embed)

    @guild_only()
    @commands.command(brief='explain the karma system to the caller based on the current configuration',
                      usage='{}explain'.format(config['prefix']))
    async def explain(self, ctx):
        embed = Embed(colour=embed_color)
        embed.title = 'Karma Tutor'
        embed.description = 'Explains the karma system under the current configuration.'
        keywords = thanks_list()
        embed.add_field(name='**General**',
                        value='Karma is a way for you to show gratitude to helpers with karma points.')
        embed.add_field(name='**How do I give karma?**',
                        value='You can give karma by including one of the following case insensitive keywords:{}'
                        .format(keywords)
                              + ' and one user mention for each helper you want to show gratitude to.')
        embed.add_field(name='**Examples**',
                        value=f'```fix\n{keywords[0]}, this really was a xy problem after all @moe.\n'
                              + 'Hey so i pondered for a while and what you said earlier was really helpful, '
                              + f'{keywords[0]} @moe @doe.\n'
                              + f'{keywords[0]} so much for @moe @doe @noe helping me out all the time.'
                              + '\n```'
                        , inline=False)
        embed.add_field(name='**What happens after giving out karma?**',
                        value='You are placed on a cooldown for the particular helper.'
                              + ' In the meantime you are still able to give karma to someone you didn\'t before.',
                        inline=False)
        embed = self.create_feedback_fields(embed)
        await ctx.channel.send(embed=embed)

    @guild_only()
    @commands.command(brief='shows the ways aura reacts based on the current configuration',
                      usage='{}reactions'.format(config['prefix']))
    async def reactions(self, ctx):
        embed = Embed(colour=embed_color)
        embed.title = 'Aura Reactions'
        await ctx.channel.send(embed=self.create_feedback_fields(embed))

    def create_feedback_fields(self, embed):
        feedback = ''
        emoji = reaction_emoji()
        if str(karma()['emote']).lower() == 'true':
            feedback += 'Aura will react with a {} to verify that you have given out karma. \n' \
                .format(emoji['karma_gain'])
        if str(karma()['time-emote']).lower() == 'true':
            feedback += 'Aura will react with a {} to show that at least one user is on a cooldown with you. \n' \
                .format(emoji['karma_cooldown'])
        if str(karma()['self_delete']).lower() == 'true':
            feedback += 'Aura will react with a {} for you to revert giving out the karma, by reacting to it.\n' \
                .format(emoji['karma_delete'])
        if str(blacklist()['emote']).lower() == 'true':
            feedback += 'Aura will react with a {} if you are blacklisted from giving out karma. \n' \
                .format(emoji['karma_blacklist'])
        if str(karma()['message']).lower() == 'true':
            feedback += 'Aura will congratulate the user/s in chat.\n'
        if str(karma()['time-message']).lower() == 'true':
            feedback += 'Aura will remind you of the cooldown in the chat.\n'
        if str(blacklist()['dm']).lower() == 'true':
            feedback += 'Aura will contact you privately, if you are blacklisted.\n'
        if str(karma()['edit']).lower() == 'true':
            feedback += 'Aura will partially track message edits.\n'
        embed.add_field(name='**Aura Feedback**', value=feedback)
        return embed

    @guild_only()
    @commands.command(brief='show all commands or show help text of a single command',
                      usage='{}help\n{}help command'.format(config['prefix'], config['prefix']))
    async def help(self, ctx, *, params: str = ""):
        args = params.split()
        log.info('Called help command with args: {}'.format(args))
        # help command only works without any arguments or one argument
        # since args can't ever be smaller than 0, this check is fine
        if len(args) <= 1:
            embed = await self.build_help_embed(ctx, args)
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send('You passed too many arguments to the help command.')

    # build the help embed that is to be returned to the user
    async def build_help_embed(self, ctx, arg) -> Embed:
        embed = Embed(colour=embed_color)
        if len(arg) == 0:
            # if no args, show help overview (all commands executable by user)
            embed = await self.overview_embed(embed, ctx)
        else:
            # show info on command in args (all commands executable by user)
            embed = await self.command_info_embed(embed, ctx, arg)
        return embed

    async def overview_embed(self, embed, ctx):
        embed.title = 'Help Menu'
        embed.description = 'Use {}help <command> for more information'.format(config['prefix'])
        cog_mapping = self.bot.cogs
        not_rendered_counter = 0
        for cog in cog_mapping:
            command_list = cog_mapping[cog].get_commands()
            if len(command_list) > 0:
                embed_val = ''
                for command in command_list:
                    # check if command is executable for caller
                    is_executable = False
                    try:
                        is_executable = await command.can_run(ctx)
                    except CommandError:
                        pass
                    if is_executable:
                        # if it is include in the embed, otherwise no need for user to know about the command.
                        embed_val += command.name + '\n'
                if embed_val != '':
                    embed.add_field(name='**' + cog + '**', value=f'```fix\n{embed_val}```', inline=True)
            else:
                not_rendered_counter -= 1
        # use the not rendered counter to insert zero width space fields to properly align the embed
        embed = add_filler_fields(embed, cog_mapping, '-', not_rendered_counter)
        return embed

    async def command_info_embed(self, embed, ctx, arg):
        # return help for the command
        command = self.bot.get_command(arg[0])
        is_executable = False
        try:
            is_executable = await command.can_run(ctx)
        except CommandError:
            pass
        # check if command exists if it does if command is executable by the user like above
        if command is not None and is_executable:
            embed.title = command.name
            embed.description = command.brief
            embed.add_field(name='**' + 'Structure' + '**', value=command.usage)
        else:
            embed.title = 'Error: Command not found'
            embed.description = 'Command does not exist or you do not have the permissions to view it'
        return embed
