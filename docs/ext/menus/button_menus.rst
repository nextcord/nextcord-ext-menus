.. currentmodule:: nextcord.ext.menus
     
.. _ext_menus_button_menus:

Using Button Menus
==================

.. contents::

Menus
~~~~~

Here is a button implementation of a basic menu that has a stop button
and two reply reactions.

Note that the :class:`ButtonMenu` class is used instead of :class:`Menu`
in order to use :class:`Button <nextcord.ui.Button>` components instead of reactions.

:class:`ButtonMenu` is a subclass of :class:`Menu` and therefore
any of the attributes and methods of :class:`Menu` are available.

Also note that ``view=self`` is passed with the initial message and
:func:`nextcord.ui.button` is used instead of :func:`menus.button() <button>`.

:meth:`ButtonMenu.disable` can be used to disable all buttons in the menu.

:meth:`ButtonMenu.enable` can be used to enable all buttons in the menu.

Additionally, :attr:`disable_buttons_after <ButtonMenu.disable_buttons_after>` can be used as a kwarg to
:class:`ButtonMenu` to disable all buttons when the menu stops and
:attr:`clear_buttons_after <ButtonMenu.clear_buttons_after>` can be used to remove them.

.. code:: py

    import nextcord
    from nextcord.ext import menus

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

Instantiation is the same as for :ref:`Reaction Menus <ext_menus_reaction_menus>`

.. code:: py

    await MyButtonMenu().start(ctx)

.. _pagination-1:

Pagination
~~~~~~~~~~

A :class:`ButtonMenuPages` class is provided for pagination with button
components.

:class:`ButtonMenuPages` works the same way as :class:`MenuPages`, but with :class:`Button <nextcord.ui.Button>` components instead of reactions.

A :class:`nextcord.ButtonStyle` can optionally be passed in to customize the
appearance of the buttons.

``MySource`` is the same as :ref:`defined earlier <MySource>`, but the menu is instantiated
with:

.. code:: py

    pages = menus.ButtonMenuPages(source=MySource(range(1, 100)), clear_buttons_after=True, 
                                  style=nextcord.ButtonStyle.primary)
    await pages.start(ctx)