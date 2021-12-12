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

The examples below are for button pagination. If you want to use reaction menus, you can simply
replace the :class:`ButtonMenuPages` with :class:`MenuPages` and replace parameters such as
``clear_buttons_after`` and ``disable_buttons_after`` with ``clear_reactions_after``.

.. contents::

Basic Pagination
----------------

In this example, we'll create a button pagination menu that shows items in a message for each page.

To get started, we will need a :class:`PageSource` object that will define how many list items to
show on each page, and how to display them. In the example below, :class:`ListPageSource` is
subclassed to provide these details: ``per_page`` is set to 4 to show four items per page and
``format_page`` is defined to display a given four entries in a message, each on a separate line.

All that is left is instantiating and starting the menu.

We will use the basic pagination class :class:`ButtonMenuPages` to handle the pagination
and pass it the page source which holds our list of entries as the ``source`` parameter.
We can optionally pass additional parameters such as the button style and any parameters
supported by :class:`ButtonMenu`. Then we can start the menu by calling 
:meth:`pages.start() <ButtonMenuPages.start>`.

.. code:: py

    from nextcord.ext import commands, menus

    bot = commands.Bot(command_prefix="$")

    class MyPageSource(menus.ListPageSource):
        def __init__(self, data):
            # this is where you can set how many items you want per page
            super().__init__(data, per_page=4)

        async def format_page(self, menu, entries):
            # this is where you can format the entries for the page
            return "\n".join(entries)

    @bot.command()
    async def pages_example(ctx):
        data = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        pages = menus.ButtonMenuPages(
            source=MyPageSource(data),
            delete_message_after=True,
        )
        await pages.start(ctx)
    
    bot.run('token')

Paginated Embeds Using Fields
-----------------------------

In this example, we will be creating an embed with fields instead of showing the entries in
message content.

Since fields have a name and value, the data we pass into the :class:`PageSource` is a list of
tuples. The first item in the tuple is the name and the second is the value.
If you do not want to be restricted to having a name and value for each item, you can use the
embed description as shown in the example that follows this one.

The entries argument in ``format_page`` will also be a list of tuples now, so we can iterate
over the entries and create a field for each using ``entry[0]`` and ``entry[1]`` as the name
and value respectively.

The return value of ``format_page`` is a :class:`nextcord.Embed` which will appear in the
message when the page is shown.

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
            ("Black", "#000000"),
            ("Blue", "#0000FF"),
            ("Brown", "#A52A2A"),
            ("Green", "#00FF00"),
            ("Grey", "#808080"),
            ("Orange", "#FFA500"),
            ("Pink", "#FFC0CB"),
            ("Purple", "#800080"),
            ("Red", "#FF0000"),
            ("White", "#FFFFFF"),
            ("Yellow", "#FFFF00"),
        ]
        pages = menus.ButtonMenuPages(
            source=MyEmbedFieldPageSource(fields),
            clear_buttons_after=True,
        )
        await pages.start(ctx)

Paginated Embeds Using Descriptions
-----------------------------------

In this example, we will use the embed description to show entries.

``data`` is a list of strings, so we can join entries with ``"\n"`` to create the description.

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

Change Button Colors
--------------------

When instantiating a :class:`ButtonMenuPages` object, you can pass a ``style`` parameter
to change the color of the buttons. You may choose from any :class:`ButtonStyle <nextcord.ButtonStyle>`
supported by Discord. These are: ``primary`` (blurple), ``secondary`` (gray), ``success`` (green), and
``danger`` (red).

.. code:: py

    @bot.command()
    async def button_style(ctx):
        data = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        pages = menus.ButtonMenuPages(
            source=MyPageSource(data),
            style=nextcord.ButtonStyle.success,
        )
        await pages.start(ctx)

Custom Emojis
-------------

To use custom emojis in pagination, you can subclass :class:`ButtonMenuPages` and override
the ``FIRST_PAGE``, ``PREVIOUS_PAGE``, ``NEXT_PAGE``. ``LAST_PAGE``, and ``STOP`` attributes.

Then, when instantiating the menu, you will use your custom class's name in place of
``menus.ButtonMenuPages``.

.. code:: py

    class CustomButtonMenuPages(menus.ButtonMenuPages):

        FIRST_PAGE = "<:pagefirst:899973860772962344>"
        PREVIOUS_PAGE = "<:pageprev:899973860965888010>"
        NEXT_PAGE = "<:pagenext:899973860840050728>"
        LAST_PAGE = "<:pagelast:899973860810694686>"
        STOP = "<:stop:899973861444042782>"

    @bot.command()
    async def custom_buttons(ctx):
        data = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        pages = CustomButtonMenuPages(source=MySource(data))
        await pages.start(ctx)

Remove Stop Button
------------------

Adding ``inherit_buttons=False`` as shown below will allow you to customize the buttons
that get displayed in the menu.

You can choose to leave out any of the buttons or add custom labels and styles using the
respective parameters to :class:`MenuPaginationButton`.

In the example below, we will remove the stop button by adding only the other four buttons.

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
            self.add_item(menus.MenuPaginationButton(emoji=self.FIRST_PAGE))
            self.add_item(menus.MenuPaginationButton(emoji=self.PREVIOUS_PAGE))
            self.add_item(menus.MenuPaginationButton(emoji=self.NEXT_PAGE))
            self.add_item(menus.MenuPaginationButton(emoji=self.LAST_PAGE))
            
            # Disable buttons that are unavailable to be pressed at the start
            self._disable_unavailable_buttons()

    @bot.command()
    async def removed_buttons(ctx):
        data = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        pages = NoStopButtonMenuPages(source=MySource(data))
        await pages.start(ctx)

GroupByPageSource
-----------------

:class:`GroupByPageSource` is an alternative to :class:`ListPageSource` that allows you to
group entries into multiple sublists similar to :func:`itertools.groupby`. Only entries
having the same group key will be displayed together on a single page. In the example below,
there are three keys: ``test``, ``other``, and ``okay``. Entries will be paginated within
each group, but when all entries from a group have been displayed, the next group will only
start on the next page.

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
    async def group_by_page_source_example(ctx):
        pages = menus.ButtonMenuPages(
            source=Source(data, key=lambda t: t.key, per_page=12),
            clear_reactions_after=True,
        )
        await pages.start(ctx)

AsyncIteratorPageSource
-----------------------

Another way to paginate is to use an :class:`AsyncIteratorPageSource` which works with async
iterators for lazy fetching of data. This is useful when you have a large amount of data to
paginate and you don't want to load all of it into memory.

Instead of a list of data, you pass a generator that yields entries as they are needed.

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
    async def async_iterator_page_source_example(ctx):
        pages = menus.ButtonMenuPages(source=Source())
        await pages.start(ctx)     

Pagination + Select Menus
-------------------------

To add additional UI components to the pagination, you can subclass :class:`ButtonMenuPages`
with ``inherit_buttons=False`` and add the buttons you want along with other components such
as a :class:`Select Menu <nextcord.ui.Select>`.

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
        data = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        pages = SelectButtonMenuPages(source=MySource(data))
        await pages.start(ctx)

Paginated Help Command Cog
--------------------------

Here is an example of a paginated help command with ``nextcord-ext-menus``.

It can be loaded as an extension just as any other :class:`Cog <nextcord.ext.commands.Cog>`.

For more details on how this can be used, check out this useful
`gist <https://gist.github.com/InterStella0/b78488fb28cadf279dfd3164b9f0cf96>`_.

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