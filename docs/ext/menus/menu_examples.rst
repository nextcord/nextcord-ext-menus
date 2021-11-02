.. _ext_menus_examples:
    
.. currentmodule:: nextcord.ext.menus

Menu Examples
=============

Here are a few examples of basic menus created with ``nextcord-ext-menus``.
Menus perform custom actions, such as updating a message, when a reaction or button is clicked.

For pagination examples, see :ref:`ext_menus_pagination_examples`.

.. contents::

Basic Reaction Menu
-------------------

.. code:: py

    import nextcord
    from nextcord.ext import commands, menus

    bot = commands.Bot(command_prefix="$")

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

    @bot.command()
    async def menu_example(ctx):
        await MyMenu().start(ctx)
    
    bot.run('token')

Wait for Confirmation
---------------------

.. code:: py

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
            
    @bot.command()
    async def delete_things(ctx):
        confirm = await Confirm('Delete everything?').prompt(ctx)
        if confirm:
            await ctx.send('deleted...')

Basic Button Menu
-----------------

.. code:: py

    class MyButtonMenu(menus.ButtonMenu):
        def __init__(self):
            super().__init__(disable_buttons_after=True)

        async def send_initial_message(self, ctx, channel):
            return await channel.send(f'Hello {ctx.author}', view=self)

        @nextcord.ui.button(emoji="\N{THUMBS UP SIGN}")
        async def on_thumbs_up(self, button, interaction):
            await self.message.edit(content=f"Thanks {interaction.user}!")

        @nextcord.ui.button(emoji="\N{THUMBS DOWN SIGN}")
        async def on_thumbs_down(self, button, interaction):
            await self.message.edit(content=f"That's not nice {interaction.user}...")

        @nextcord.ui.button(emoji="\N{BLACK SQUARE FOR STOP}\ufe0f")
        async def on_stop(self, button, interaction):
            self.stop()

    @bot.command()
    async def button_menu_example(ctx):
        await MyButtonMenu().start(ctx)

Button Confirm
--------------

.. code:: py

    class ButtonConfirm(menus.ButtonMenu):
        def __init__(self, msg):
            super().__init__(timeout=15.0, clear_buttons_after=True)
            self.msg = msg
            self.result = None

        async def send_initial_message(self, ctx, channel):
            return await channel.send(self.msg, view=self)

        @nextcord.ui.button(emoji="\N{WHITE HEAVY CHECK MARK}")
        async def do_confirm(self, button, interaction):
            self.result = True
            self.stop()

        @nextcord.ui.button(emoji="\N{CROSS MARK}")
        async def do_deny(self, button, interaction):
            self.result = False
            self.stop()

        async def prompt(self, ctx):
            await menus.Menu.start(self, ctx, wait=True)
            return self.result

    @bot.command()
    async def button_confirm(ctx: commands.Context):
        confirm = await ButtonConfirm("Confirm?").prompt(ctx)
        await ctx.send(f"You said: {confirm}")
