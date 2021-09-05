"""
This is an example of a Help Cog with button component pagination.

The basic embed help command is based on this gist by Rapptz:
https://gist.github.com/Rapptz/31a346ed1eb545ddeb0d451d81a60b3b
"""

from dataclasses import dataclass

import nextcord
from nextcord.ext import commands, menus

from config import PREFIX


@dataclass
class EmbedField:
    name: str
    value: str
    inline: bool


class HelpPages(menus.ListPageSource):
    def __init__(self, help_command, data):
        self._help_command = help_command
        # you can set here how many items to display per page
        super().__init__(data, per_page=2)

    async def format_page(self, menu, entries):
        """
        Returns an embed containing the entries for the current page
        """
        invoked_with = self._help_command.invoked_with
        embed = nextcord.Embed(title="Bot Commands",
                               colour=self._help_command.COLOUR)
        embed.description = (
            f'Use "{PREFIX}{invoked_with} command" for more info on a command.\n'
            f'Use "{PREFIX}{invoked_with} category" for more info on a category.'
        )
        for entry in entries:
            embed.add_field(name=entry.name, value=entry.value,
                            inline=entry.inline)
        return embed


class NewHelpCommand(commands.MinimalHelpCommand):
    """Custom help command override using embeds"""

    # embed colour
    COLOUR = nextcord.Colour.blurple()

    def get_command_signature(self, command: commands.core.Command):
        """Retrieves the signature portion of the help page."""
        return f"{PREFIX}{command.qualified_name} {command.signature}"

    async def send_bot_help(self, mapping: dict):
        """implements bot command help page"""
        invoked_with = self.invoked_with
        embed = nextcord.Embed(title="Bot Commands", colour=self.COLOUR)
        embed.description = (
            f'Use "{PREFIX}{invoked_with} command" for more info on a command.\n'
            f'Use "{PREFIX}{invoked_with} category" for more info on a category.'
        )

        embed_fields = []

        for cog, commands in mapping.items():
            name = "No Category" if cog is None else cog.qualified_name
            filtered = await self.filter_commands(commands, sort=True)
            if filtered:
                # \u2002 = en space
                value = "\u2002".join(f"`{PREFIX}{c.name}`" for c in filtered)
                if cog and cog.description:
                    value = f"{cog.description}\n{value}"
                # add EmbedField object to the list of fields
                embed_fields.append(EmbedField(name=name, value=value, inline=True))

        # create a pagination menu that paginates the fields
        pages = menus.ButtonMenuPages(source=HelpPages(self, embed_fields), clear_buttons_after=True)
        await pages.start(self.context)

    async def send_cog_help(self, cog: commands.Cog):
        """implements cog help page"""
        embed = nextcord.Embed(
            title=f"{cog.qualified_name} Commands", colour=self.COLOUR
        )
        if cog.description:
            embed.description = cog.description

        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered:
            embed.add_field(
                name=self.get_command_signature(command),
                value=command.short_doc or "...",
                inline=False,
            )

        embed.set_footer(
            text=f"Use {PREFIX}help [command] for more info on a command.")
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group: commands.Group):
        """implements group help page and command help page"""
        embed = nextcord.Embed(title=group.qualified_name, colour=self.COLOUR)
        if group.help:
            embed.description = group.help

        if isinstance(group, commands.Group):
            filtered = await self.filter_commands(group.commands, sort=True)
            for command in filtered:
                embed.add_field(
                    name=self.get_command_signature(command),
                    value=command.short_doc or "...",
                    inline=False,
                )

        await self.get_destination().send(embed=embed)

    # Use the same function as group help for command help
    send_command_help = send_group_help


class HelpCog(commands.Cog, name="Help"):
    """Displays help information for commands and cogs"""

    def __init__(self, bot: commands.Bot):
        self.__bot = bot
        self.__original_help_command = bot.help_command
        bot.help_command = NewHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.__bot.help_command = self.__original_help_command


def setup(bot: commands.Bot):
    bot.add_cog(HelpCog(bot))
