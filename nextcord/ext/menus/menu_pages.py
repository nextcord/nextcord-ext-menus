from typing import Any, List, Optional

import nextcord
from nextcord.ext import commands

from .constants import PageFormatType, SendKwargsType
from .menus import Button, ButtonMenu, Menu
from .page_source import PageSource
from .utils import First, Last, _cast_emoji


class MenuPagesBase(Menu):
    """A base class dedicated to pagination for reaction and button menus.

    Attributes
    ------------
    current_page: :class:`int`
        The current page that we are in. Zero-indexed
        between [0, :attr:`PageSource.max_pages`).
    """

    FIRST_PAGE = "\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}\ufe0f"
    PREVIOUS_PAGE = "\N{BLACK LEFT-POINTING TRIANGLE}\ufe0f"
    NEXT_PAGE = "\N{BLACK RIGHT-POINTING TRIANGLE}\ufe0f"
    LAST_PAGE = "\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}\ufe0f"
    STOP = "\N{BLACK SQUARE FOR STOP}\ufe0f"

    def __init__(self, source: PageSource, **kwargs):
        self._source = source
        self.current_page = 0
        if hasattr(self, "__button_menu_pages__"):
            ButtonMenu.__init__(self, **kwargs)
            return
        Menu.__init__(self, **kwargs)

    @property
    def source(self) -> PageSource:
        """:class:`PageSource`: The source where the data comes from."""
        return self._source

    async def change_source(self, source: PageSource):
        """|coro|

        Changes the :class:`PageSource` to a different one at runtime.

        Once the change has been set, the menu is moved to the first
        page of the new source if it was started. This effectively
        changes the :attr:`current_page` to 0.

        Raises
        --------
        TypeError
            A :class:`PageSource` was not passed.
        """

        if not isinstance(source, PageSource):
            raise TypeError(
                "Expected {0!r} not {1.__class__!r}.".format(PageSource, source)
            )

        self._source = source
        self.current_page = 0
        if self.message is not None:
            await source._prepare_once()
            await self.show_page(0)

    def should_add_reactions(self) -> bool:
        return self.should_add_reactions_or_buttons()

    def should_add_buttons(self) -> bool:
        return self.should_add_reactions_or_buttons()

    def should_add_reactions_or_buttons(self) -> bool:
        return self._source.is_paginating()

    async def _get_kwargs_from_page(self, page: List[Any]) -> SendKwargsType:
        """|coro|

        Calls :meth:`PageSource.format_page` and returns a dict of send kwargs

        Raises
        --------
        TypeError
            The return value of :meth:`PageSource.format_page` was not a
            :class:`str`, :class:`nextcord.Embed`, :class:`List[nextcord.Embed]`,
            or :class:`dict`.
        """
        value: PageFormatType = await nextcord.utils.maybe_coroutine(
            self._source.format_page, self, page
        )
        if isinstance(value, dict):
            return value
        elif isinstance(value, str):
            return {"content": value}
        elif isinstance(value, nextcord.Embed):
            return {"embed": value}
        elif isinstance(value, list) and all(
            isinstance(v, nextcord.Embed) for v in value
        ):
            return {"embeds": value}
        raise TypeError(
            "Expected {0!r} not {1.__class__!r}.".format(
                (dict, str, nextcord.Embed, List[nextcord.Embed]), value
            )
        )

    async def show_page(self, page_number: int):
        """|coro|

        Sets the current page to the specified page and shows it.
        """
        page = await self._source.get_page(page_number)
        self.current_page = page_number
        kwargs = await self._get_kwargs_from_page(page)
        await self.message.edit(**kwargs)

    async def send_initial_message(
        self, ctx: commands.Context, channel: nextcord.abc.Messageable
    ) -> nextcord.Message:
        """|coro|

        The default implementation of :meth:`Menu.send_initial_message`
        for the interactive pagination session.

        This implementation shows the first page of the source.
        """
        page = await self._source.get_page(0)
        kwargs = await self._get_kwargs_from_page(page)
        # filter out kwargs that are "None"
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        # if there is an interaction, send an interaction response
        if self.interaction is not None:
            message = await self.interaction.send(ephemeral=self.ephemeral, **kwargs)
            return message or await self.interaction.original_message()
        # otherwise, send the message using the channel
        return await channel.send(**kwargs)

    async def start(
        self,
        ctx: Optional[commands.Context] = None,
        interaction: Optional[nextcord.Interaction] = None,
        *,
        channel: Optional[nextcord.abc.Messageable] = None,
        wait: bool = False,
        ephemeral: bool = False,
    ):
        await self._source._prepare_once()
        await super().start(
            ctx=ctx,
            interaction=interaction,
            channel=channel,
            wait=wait,
            ephemeral=ephemeral,
        )
        # If we're not paginating, we can remove the pagination buttons
        if not self._source.is_paginating():
            await self.clear()

    async def show_checked_page(self, page_number: int):
        max_pages = self._source.get_max_pages()
        try:
            # If it doesn't give maximum pages, it cannot be checked
            if max_pages is None or max_pages > page_number >= 0:
                await self.show_page(page_number)
        except IndexError:
            # An error happened that can be handled, so ignore it.
            pass

    async def show_current_page(self):
        if self._source.is_paginating():
            await self.show_page(self.current_page)

    def _skip_double_triangle_buttons(self) -> bool:
        max_pages = self._source.get_max_pages()
        if max_pages is None:
            return True
        return max_pages <= 2

    async def go_to_first_page(self, payload=None):
        """go to the first page"""
        await self.show_page(0)

    async def go_to_previous_page(self, payload=None):
        """go to the previous page"""
        await self.show_checked_page(self.current_page - 1)

    async def go_to_next_page(self, payload=None):
        """go to the next page"""
        await self.show_checked_page(self.current_page + 1)

    async def go_to_last_page(self, payload=None):
        """go to the last page"""
        # The call here is safe because it's guarded by skip_if
        await self.show_page(self._source.get_max_pages() - 1)

    async def stop_pages(self, payload=None):
        """stops the pagination session."""
        self.stop()


class MenuPages(MenuPagesBase):
    """A special type of Menu dedicated to pagination with reactions.

    Attributes
    ------------
    current_page: :class:`int`
        The current page that we are in. Zero-indexed
        between [0, :attr:`PageSource.max_pages`).
    """

    def __init__(self, source: PageSource, **kwargs):
        super().__init__(source, **kwargs)
        # skip adding buttons if inherit_buttons=False was passed to metaclass
        if not self.__inherit_buttons__:
            return
        # add pagination reaction buttons
        self.add_button(
            Button(
                self.FIRST_PAGE,
                self.go_to_first_page,
                position=First(0),
                skip_if=self._skip_double_triangle_buttons,
            ),
        )
        self.add_button(
            Button(self.PREVIOUS_PAGE, self.go_to_previous_page, position=First(1))
        )
        self.add_button(
            Button(self.NEXT_PAGE, self.go_to_next_page, position=Last(0)),
        )
        self.add_button(
            Button(
                self.LAST_PAGE,
                self.go_to_last_page,
                position=Last(1),
                skip_if=self._skip_double_triangle_buttons,
            ),
        )
        self.add_button(
            Button(self.STOP, self.stop_pages, position=Last(2)),
        )


class MenuPaginationButton(nextcord.ui.Button["MenuPaginationButton"]):
    """
    A custom button for pagination used by :class:`ButtonMenuPages`
    that runs pagination methods in the :meth:`MenuPaginationButton.callback`
    corresponding to the emoji.

    This is a subclass of :class:`nextcord.ui.Button` and as
    such, accepts all of its parameters.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        emoji = kwargs.get("emoji", None)
        self._emoji = _cast_emoji(emoji) if emoji else None

    async def callback(self, interaction: nextcord.Interaction):
        """
        Callback for when this button is pressed
        """
        if self._emoji is None:
            return

        assert self.view is not None
        view: ButtonMenuPages = self.view

        # change the current page
        if str(self._emoji) == view.FIRST_PAGE:
            await view.go_to_first_page()
        elif str(self._emoji) == view.PREVIOUS_PAGE:
            await view.go_to_previous_page()
        elif str(self._emoji) == view.NEXT_PAGE:
            await view.go_to_next_page()
        elif str(self._emoji) == view.LAST_PAGE:
            await view.go_to_last_page()
        elif str(self._emoji) == view.STOP:
            await view.stop_pages()


class ButtonMenuPages(MenuPagesBase, ButtonMenu):
    """A special type of Menu dedicated to pagination with button components.

    Parameters
    -----------
    style: :class:`nextcord.ui.ButtonStyle`
        The button style to use for the pagination buttons.

    Attributes
    ------------
    current_page: :class:`int`
        The current page that we are in. Zero-indexed
        between [0, :attr:`PageSource.max_pages`).
    """

    def __init__(
        self,
        source: PageSource,
        style: nextcord.ButtonStyle = nextcord.ButtonStyle.secondary,
        **kwargs,
    ):
        self.__button_menu_pages__ = True
        # make button pagination disable buttons on stop by default unless it's overridden
        if "disable_buttons_after" not in kwargs:
            kwargs["disable_buttons_after"] = True
        super().__init__(source, **kwargs)
        # skip adding buttons if inherit_buttons=False was passed to metaclass or only one page
        if not self.__inherit_buttons__ or not self.should_add_buttons():
            return
        # add buttons to the view
        pagination_emojis = (
            self.FIRST_PAGE,
            self.PREVIOUS_PAGE,
            self.NEXT_PAGE,
            self.LAST_PAGE,
            self.STOP,
        )
        double_triangle_emojis = {self.FIRST_PAGE, self.LAST_PAGE}
        for emoji in pagination_emojis:
            if emoji in double_triangle_emojis and self._skip_double_triangle_buttons():
                continue
            self.add_item(MenuPaginationButton(emoji=emoji, style=style))
        # disable buttons that are not available
        self._disable_unavailable_buttons()

    async def show_page(self, page_number: int):
        """|coro|
        Sets the current page to the specified page and shows it.
        """
        # disable buttons that are not available
        self.current_page = page_number
        self._disable_unavailable_buttons()
        # show the page
        await super().show_page(page_number)

    async def _get_kwargs_from_page(self, page: List[Any]) -> SendKwargsType:
        """|coro|
        Calls :meth:`PageSource.format_page` and returns a dict of send kwargs

        Raises
        --------
        TypeError
            The return value of :meth:`PageSource.format_page` was not a
            :class:`str`, :class:`nextcord.Embed`, :class:`List[nextcord.Embed]`,
            or :class:`dict`.
        """
        kwargs = await super()._get_kwargs_from_page(page)
        # add view to kwargs if it's not already there
        return {"view": self, **kwargs}

    def _disable_unavailable_buttons(self):
        """
        Disables buttons that are unavailable to be pressed.
        """
        children: List[MenuPaginationButton] = self.children
        max_pages = self._source.get_max_pages()
        for child in children:
            if isinstance(child, nextcord.ui.Button):
                if str(child.emoji) in (self.FIRST_PAGE, self.PREVIOUS_PAGE):
                    child.disabled = self.current_page == 0
                elif max_pages and str(child.emoji) in (self.LAST_PAGE, self.NEXT_PAGE):
                    child.disabled = self.current_page == max_pages - 1
