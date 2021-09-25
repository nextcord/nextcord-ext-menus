from typing import Any, List, Optional

import nextcord
from nextcord.ext import commands

from .constants import EmojiType, PageFormatType, SendKwargsType
from .menus import ButtonMenu, Menu, button
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
    FIRST_PAGE = '\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}\ufe0f'
    PREVIOUS_PAGE = '\N{BLACK LEFT-POINTING TRIANGLE}\ufe0f'
    NEXT_PAGE = '\N{BLACK RIGHT-POINTING TRIANGLE}\ufe0f'
    LAST_PAGE = '\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}\ufe0f'
    STOP = '\N{BLACK SQUARE FOR STOP}\ufe0f'

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
                'Expected {0!r} not {1.__class__!r}.'.format(PageSource, source))

        self._source = source
        self.current_page = 0
        if self.message is not None:
            await source._prepare_once()
            await self.show_page(0)

    def should_add_reactions(self) -> bool:
        return self.should_add_reactions_or_buttons()

    def should_add_reactions_or_buttons(self) -> bool:
        return self._source.is_paginating()

    async def _get_kwargs_from_page(self, page: List[Any]) -> SendKwargsType:
        value: PageFormatType = await nextcord.utils.maybe_coroutine(self._source.format_page, self, page)
        if isinstance(value, dict):
            return value
        elif isinstance(value, str):
            return {'content': value, 'embed': None}
        elif isinstance(value, nextcord.Embed):
            return {'embed': value, 'content': None}

    async def show_page(self, page_number: int):
        page = await self._source.get_page(page_number)
        self.current_page = page_number
        kwargs = await self._get_kwargs_from_page(page)
        await self.message.edit(**kwargs)

    async def send_initial_message(self, ctx: commands.Context, channel: nextcord.abc.Messageable) -> nextcord.Message:
        """|coro|

        The default implementation of :meth:`Menu.send_initial_message`
        for the interactive pagination session.

        This implementation shows the first page of the source.
        """
        page = await self._source.get_page(0)
        kwargs = await self._get_kwargs_from_page(page)
        if hasattr(self, '__discord_ui_view__'):
            kwargs['view'] = self
        return await channel.send(**kwargs)

    async def start(self, ctx: commands.Context, *, channel: Optional[nextcord.abc.Messageable] = None, wait: Optional[bool] = False):
        await self._source._prepare_once()
        await super().start(ctx, channel=channel, wait=wait)

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

    @button(MenuPagesBase.FIRST_PAGE, position=First(0), skip_if=MenuPagesBase._skip_double_triangle_buttons)
    async def go_to_first_page(self, payload):
        """go to the first page"""
        await self.show_page(0)

    @button(MenuPagesBase.PREVIOUS_PAGE, position=First(1))
    async def go_to_previous_page(self, payload):
        """go to the previous page"""
        await self.show_checked_page(self.current_page - 1)

    @button(MenuPagesBase.NEXT_PAGE, position=Last(0))
    async def go_to_next_page(self, payload):
        """go to the next page"""
        await self.show_checked_page(self.current_page + 1)

    @button(MenuPagesBase.LAST_PAGE, position=Last(1), skip_if=MenuPagesBase._skip_double_triangle_buttons)
    async def go_to_last_page(self, payload):
        """go to the last page"""
        # The call here is safe because it's guarded by skip_if
        await self.show_page(self._source.get_max_pages() - 1)

    @button(MenuPagesBase.STOP, position=Last(2))
    async def stop_pages(self, payload):
        """stops the pagination session."""
        self.stop()


class MenuPaginationButton(nextcord.ui.Button['MenuPaginationButton']):
    """
    A custom button for pagination that will be disabled when unavailable.
    """

    def __init__(self, style: nextcord.ButtonStyle, emoji: EmojiType):
        super().__init__(style=style, emoji=emoji)
        self._emoji = _cast_emoji(emoji)

    async def callback(self, interaction: nextcord.Interaction):
        """
        Callback for when this button is pressed
        """
        assert self.view is not None
        view: ButtonMenuPages = self.view

        # change the current page
        if self._emoji.name == view.FIRST_PAGE:
            await view.show_page(0)
        elif self._emoji.name == view.PREVIOUS_PAGE:
            await view.show_checked_page(view.current_page - 1)
        elif self._emoji.name == view.NEXT_PAGE:
            await view.show_checked_page(view.current_page + 1)
        elif self._emoji.name == view.LAST_PAGE:
            await view.show_page(view._source.get_max_pages() - 1)

        # disable buttons that are unavailable
        view._disable_unavailable_buttons()

        # disable all buttons if stop is pressed
        if self._emoji.name == view.STOP:
            await view.disable()
            view.stop()

        # update the view
        await interaction.response.edit_message(view=view)


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

    def __init__(self, source: PageSource, style: nextcord.ButtonStyle = nextcord.ButtonStyle.secondary, **kwargs):
        self.__button_menu_pages__ = True
        super().__init__(source, **kwargs)
        # skip adding buttons if inherit_buttons=False was passed to metaclass
        if not self.__inherit_buttons__:
            return
        # add buttons to the view
        for emoji in (self.FIRST_PAGE, self.PREVIOUS_PAGE, self.NEXT_PAGE, self.LAST_PAGE, self.STOP):
            if emoji in {self.FIRST_PAGE, self.LAST_PAGE} and self._skip_double_triangle_buttons():
                continue
            self.add_item(MenuPaginationButton(style=style, emoji=emoji))
        self._disable_unavailable_buttons()

    def _disable_unavailable_buttons(self):
        """
        Disables buttons that are unavailable to be pressed.
        """
        buttons: List[MenuPaginationButton] = self.children
        max_pages = self._source.get_max_pages()
        for button in buttons:
            if button.emoji.name in (self.FIRST_PAGE, self.PREVIOUS_PAGE):
                button.disabled = self.current_page == 0
            elif max_pages and button.emoji.name in (self.LAST_PAGE, self.NEXT_PAGE):
                button.disabled = self.current_page == max_pages - 1
