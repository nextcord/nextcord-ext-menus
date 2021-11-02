.. _ext_menus_pagination_examples:

.. currentmodule:: nextcord.ext.menus

Pagination Examples
===================

Here are few examples of pagination with ``nextcord-ext-menus``.

The built-in pagination classes (:class:`MenuPages` and :class:`ButtonMenuPages`)
handle splitting data into pages, sending the initial message, timeout actions, and button actions for
:meth:`first page <MenuPages.go_to_first_page>`, :meth:`previous page <MenuPages.go_to_previous_page>`, 
:meth:`next page <MenuPages.go_to_next_page>`, :meth:`last page <MenuPages.go_to_last_page>`, 
and :meth:`stop <MenuPages.stop_pages>` all for you.

.. contents::

Basic Pagination
----------------

.. code:: py

    import nextcord
    from nextcord.ext import commands, menus

    bot = commands.Bot(command_prefix="$")

    class MyPageSource(menus.ListPageSource):
        def __init__(self, data):
            super().__init__(data, per_page=4)

        async def format_page(self, menu, entries):
            return "\n".join(entries)

    @bot.command()
    async def pages(ctx):
        entries = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        pages = menus.ButtonMenuPages(
            source=MyPageSource(entries),
            delete_message_after=True,
        )
        await pages.start(ctx)
    
    bot.run('token')

Paginated Embeds Using Fields
-----------------------------

.. code:: py

    class MyEmbedFieldPageSource(menus.ListPageSource):
        def __init__(self, data):
            super().__init__(data, per_page=4)

        async def format_page(self, menu, entries):
            embed = nextcord.Embed(title="Entries")
            for entry in entries:
                embed.add_field(name=entry[0], value=entry[1], inline=True)
            embed.set_footer(text=f'Page {menu.current_page + 1}/{self.get_max_pages()}')
            return embed

    @bot.command()
    async def button_embed_field(ctx):
        fields = [
            ["Black", "#000000"],
            ["Blue", "#0000FF"],
            ["Brown", "#A52A2A"],
            ["Green", "#00FF00"],
            ["Grey", "#808080"],
            ["Orange", "#FFA500"],
            ["Pink", "#FFC0CB"],
            ["Purple", "#800080"],
            ["Red", "#FF0000"],
            ["White", "#FFFFFF"],
            ["Yellow", "#FFFF00"],
        ]
        pages = menus.ButtonMenuPages(
            source=MyEmbedFieldPageSource(fields),
            clear_buttons_after=True,
        )
        await pages.start(ctx)

Paginated Embeds Using Descriptions
-----------------------------------

.. code:: py

    class MyEmbedDescriptionPageSource(menus.ListPageSource):
        def __init__(self, data):
            super().__init__(data, per_page=6)

        async def format_page(self, menu, entries):
            embed = Embed(title="Entries", description="\n".join(entries))
            embed.set_footer(text=f'Page {menu.current_page + 1}/{self.get_max_pages()}')
            return embed


    @bot.command()
    async def button_embed_description(ctx):
        data = [f'Description for entry #{num}' for num in range(1, 51)]
        pages = menus.ButtonMenuPages(
            source=MyEmbedDescriptionPageSource(data),
            disable_buttons_after=True,
        )
        await pages.start(ctx)

Custom Emojis
-------------

.. code:: py

    class CustomButtonMenuPages(menus.ButtonMenuPages):

        FIRST_PAGE = "<:pagefirst:899973860772962344>"
        PREVIOUS_PAGE = "<:pageprev:899973860965888010>"
        NEXT_PAGE = "<:pagenext:899973860840050728>"
        LAST_PAGE = "<:pagelast:899973860810694686>"
        STOP = "<:stop:899973861444042782>"

    @bot.command()
    async def custom_buttons(ctx):
        pages = CustomButtonMenuPages(source=MySource(range(1, 100)))
        await pages.start(ctx)

Remove Stop Button
------------------

.. code:: py

    class NoStopButtonMenuPages(menus.ButtonMenuPages, inherit_buttons=False):
        """
        This class overrides the default ButtonMenuPages without inheriting the buttons
        by setting inherit_buttons to False.

        This allows us to add our own buttons with custom labels, styles, or even callbacks. 
        """

        def __init__(self, source, timeout=60):
            super().__init__(source, timeout=timeout)
            
            # Add the buttons we want
            self.add_item(menus.MenuPaginationButton(emoji=self.FIRST_PAGE, label="First"))
            self.add_item(menus.MenuPaginationButton(emoji=self.PREVIOUS_PAGE, label="Prev"))
            self.add_item(menus.MenuPaginationButton(emoji=self.NEXT_PAGE, label="Next"))
            self.add_item(menus.MenuPaginationButton(emoji=self.LAST_PAGE, label="Last"))
            
            # Disable buttons that are unavailable to be pressed at the start
            self._disable_unavailable_buttons()

    @bot.command()
    async def removed_buttons(ctx):
        pages = NoStopButtonMenuPages(source=MySource(range(1, 100)))
        await pages.start(ctx)

GroupByPageSource
-----------------

.. code:: py

    class Test:
        def __init__(self, key, value):
            self.key = key
            self.value = value

    data = [
        Test(key=key, value=value)
        for key in ['test', 'other', 'okay']
        for value in range(20)
    ]

    class Source(menus.GroupByPageSource):
        async def format_page(self, menu, entry):
            joined = '\n'.join(f'{i}. <Test value={v.value}>' for i, v in enumerate(entry.items, start=1))
            return f'**{entry.key}**\n{joined}\nPage {menu.current_page + 1}/{self.get_max_pages()}'

    @bot.command()
    async def group_by_page_source_example(ctx: commands.Context):
        pages = menus.ButtonMenuPages(
            source=Source(data, key=lambda t: t.key, per_page=12),
            clear_reactions_after=True,
        )
        await pages.start(ctx)

AsyncIteratorPageSource
-----------------------

.. code:: py

    class Test:
        def __init__(self, value):
            self.value = value

        def __repr__(self):
            return f'<Test value={self.value}>'

    async def generate(number):
        for i in range(number):
            yield Test(i)

    class Source(menus.AsyncIteratorPageSource):
        def __init__(self):
            super().__init__(generate(9), per_page=4)

        async def format_page(self, menu, entries):
            start = menu.current_page * self.per_page
            return f'\n'.join(f'{i}. {v!r}' for i, v in enumerate(entries, start=start))

    @bot.command()
    async def async_iterator_page_source_example(ctx: commands.Context):
        pages = menus.ButtonMenuPages(source=Source())
        await pages.start(ctx)     

Pagination + Select Menus
-------------------------

See `Nextcord's dropdown example <https://github.com/nextcord/nextcord/blob/master/examples/views/dropdown.py>`_
for an example on how to create a :class:`Select Menu <nextcord.ui.Select>`.

.. code:: py

    class SelectButtonMenuPages(menus.ButtonMenuPages, inherit_buttons=False):
        def __init__(self, source: menus.PageSource, timeout: int = 60):
            super().__init__(source, timeout=timeout, disable_buttons_after=True)
            self.add_item(MenuPaginationButton(emoji=self.FIRST_PAGE))
            self.add_item(MenuPaginationButton(emoji=self.PREVIOUS_PAGE))
            self.add_item(MenuPaginationButton(emoji=self.NEXT_PAGE))
            self.add_item(MenuPaginationButton(emoji=self.LAST_PAGE))
            self.add_item(MyDropdown())
            self._disable_unavailable_buttons()

    @bot.command()
    async def button_select_pages(ctx):
        pages = SelectButtonMenuPages(source=MySource(range(1, 100)))
        await pages.start(ctx)

Paginated Help Command Cog
--------------------------

.. code:: py

    from typing import List, Tuple

    import nextcord
    from nextcord.ext import commands, menus


    class HelpPageSource(menus.ListPageSource):
        """Page source for dividing the list of tuples into pages and displaying them in embeds"""

        def __init__(self, help_command: "NewHelpCommand", data: List[Tuple[str, str]]):
            self._help_command = help_command
            # you can set here how many items to display per page
            super().__init__(data, per_page=2)

        async def format_page(self, menu: menus.ButtonMenuPages, entries: List[Tuple[str, str]]):
            """
            Returns an embed containing the entries for the current page
            """
            prefix = self._help_command.context.clean_prefix
            invoked_with = self._help_command.invoked_with
            # create embed
            embed = nextcord.Embed(title="Bot Commands", colour=self._help_command.COLOUR)
            embed.description = (
                f'Use "{prefix}{invoked_with} command" for more info on a command.\n'
                f'Use "{prefix}{invoked_with} category" for more info on a category.'
            )
            # add the entries to the embed
            for entry in entries:
                embed.add_field(name=entry[0], value=entry[1], inline=True)
            # set the footer to display the page number
            embed.set_footer(text=f'Page {menu.current_page + 1}/{self.get_max_pages()}')
            return embed


    class HelpButtonMenuPages(menus.ButtonMenuPages):
        """Subclass of ButtonMenuPages to add an interaction_check"""

        def __init__(self, ctx: commands.Context, **kwargs):
            super().__init__(**kwargs)
            self._ctx = ctx

        async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
            """Ensure that the user of the button is the one who called the help command"""
            return self._ctx.author == interaction.user


    class NewHelpCommand(commands.MinimalHelpCommand):
        """Custom help command override using embeds and button pagination"""

        # embed colour
        COLOUR = nextcord.Colour.blurple()

        def get_command_signature(self, command: commands.core.Command):
            """Retrieves the signature portion of the help page."""
            return f"{self.context.clean_prefix}{command.qualified_name} {command.signature}"

        async def send_bot_help(self, mapping: dict):
            """implements bot command help page"""
            prefix = self.context.clean_prefix
            invoked_with = self.invoked_with
            embed = nextcord.Embed(title="Bot Commands", colour=self.COLOUR)
            embed.description = (
                f'Use "{prefix}{invoked_with} command" for more info on a command.\n'
                f'Use "{prefix}{invoked_with} category" for more info on a category.'
            )

            # create a list of tuples for the page source
            embed_fields = []
            for cog, commands in mapping.items():
                name = "No Category" if cog is None else cog.qualified_name
                filtered = await self.filter_commands(commands, sort=True)
                if filtered:
                    # \u2002 = en space
                    value = "\u2002".join(f"`{prefix}{c.name}`" for c in filtered)
                    if cog and cog.description:
                        value = f"{cog.description}\n{value}"
                    # add (name, value) pair to the list of fields
                    embed_fields.append((name, value))

            # create a pagination menu that paginates the fields
            pages = HelpButtonMenuPages(
                ctx=self.context,
                source=HelpPageSource(self, embed_fields),
                disable_buttons_after=True
            )
            await pages.start(self.context)

        async def send_cog_help(self, cog: commands.Cog):
            """implements cog help page"""
            embed = nextcord.Embed(
                title=f"{cog.qualified_name} Commands",
                colour=self.COLOUR,
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
                text=f"Use {self.context.clean_prefix}help [command] for more info on a command."
            )
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