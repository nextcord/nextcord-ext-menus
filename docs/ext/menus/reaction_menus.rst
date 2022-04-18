.. currentmodule:: nextcord.ext.menus

.. _ext_menus_reaction_menus:

Using Reaction Menus
====================

.. contents::

Menus
~~~~~

To whet your appetite, the following examples show the fundamentals on
how to create reaction menus.

The first example shows a basic menu that has a stop button and two
reply buttons:

.. code:: py

    from nextcord.ext import menus

    class MyMenu(menus.Menu):
        async def send_initial_message(self, ctx, channel):
            return await channel.send(f'Hello {ctx.author}')

        @menus.button('\N{THUMBS UP SIGN}')
        async def on_thumbs_up(self, payload):
            await self.message.edit(content=f'Thanks {self.ctx.author}!')

        @menus.button('\N{THUMBS DOWN SIGN}')
        async def on_thumbs_down(self, payload):
            await self.message.edit(content=f"That's not nice {self.ctx.author}...")

        @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f')
        async def on_stop(self, payload):
            self.stop()

Now, within a command we just instantiate it and we start it like so:

.. code:: py

    @bot.command()
    async def menu_example(ctx):
        await MyMenu().start(ctx)

If an error happens, then an exception of type :class:`MenuError` is
raised.

This second example shows a confirmation menu and how we can compose it
and use it later:

.. code:: py

    from nextcord.ext import menus

    class Confirm(menus.Menu):
        def __init__(self, msg):
            super().__init__(timeout=30.0, delete_message_after=True)
            self.msg = msg
            self.result = None

        async def send_initial_message(self, ctx, channel):
            return await channel.send(self.msg)

        @menus.button('\N{WHITE HEAVY CHECK MARK}')
        async def do_confirm(self, payload):
            self.result = True
            self.stop()

        @menus.button('\N{CROSS MARK}')
        async def do_deny(self, payload):
            self.result = False
            self.stop()

        async def prompt(self, ctx):
            await self.start(ctx, wait=True)
            return self.result

Then when it comes time to use it we can do it like so:

.. code:: py

    @bot.command()
    async def delete_things(ctx):
        confirm = await Confirm('Delete everything?').prompt(ctx)
        if confirm:
            await ctx.send('deleted...')

Pagination
~~~~~~~~~~

The meat of the library is the :class:`Menu` class but a :class:`MenuPages` class
is provided for the common use case of actually making a pagination
session.

The :class:`MenuPages` works similar to :class:`Menu` except things are separated
into a :class:`PageSource`. The actual :class:`MenuPages` rarely needs to be
modified, instead we pass in a :class:`PageSource` that deals with the data
representation and formatting of the data we want to paginate.

The library comes with a few built-in page sources:

-  :class:`ListPageSource`: The basic source that deals with a list of items.
-  :class:`GroupByPageSource`: A page source that groups a list into multiple sublists similar to :func:`itertools.groupby`.
-  :class:`AsyncIteratorPageSource`: A page source that works with async iterators for lazy fetching of data.

None of these page sources deal with formatting of data, leaving that up
to you.

For the sake of example, here’s a basic list source that is paginated:

.. _MySource:

.. code:: py

    from nextcord.ext import menus

    class MySource(menus.ListPageSource):
        def __init__(self, data):
            super().__init__(data, per_page=4)

        async def format_page(self, menu, entries):
            offset = menu.current_page * self.per_page
            return '\n'.join(f'{i}. {v}' for i, v in enumerate(entries, start=offset))

    @bot.command()
    async def pages_example(ctx):
        data = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        pages = menus.MenuPages(source=MySource(data), clear_reactions_after=True)
        await pages.start(ctx)

The :meth:`PageSource.format_page` can return either a :class:`str` for content,
:class:`nextcord.Embed` for an embed, List[:class:`nextcord.Embed`] for
sending multiple embeds, or a :class:`dict` to pass into the kwargs
of :meth:`nextcord.Message.edit`.
