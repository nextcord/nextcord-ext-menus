import nextcord
from nextcord.ext import commands, menus


bot = commands.Bot(command_prefix="$")


class CustomButtonMenuPages(menus.ButtonMenuPages, inherit_buttons=False):
    """
    This class overrides the default ButtonMenuPages without inheriting the buttons
    by setting inherit_buttons to False.

    This allows us to add our own buttons with custom labels, colors, or even callbacks. 
    """

    def __init__(self, source, timeout=60):
        super().__init__(source, timeout=timeout)
        # Note: for the default button callback to work, the emoji must be the same.
        # None of the buttons are required; you can leave any of them out.
        self.add_item(menus.MenuPaginationButton(emoji=self.FIRST_PAGE, label="First"))
        self.add_item(menus.MenuPaginationButton(emoji=self.PREVIOUS_PAGE, label="Prev"))
        self.add_item(menus.MenuPaginationButton(emoji=self.NEXT_PAGE, label="Next"))
        self.add_item(menus.MenuPaginationButton(emoji=self.LAST_PAGE, label="Last"))
        # place the Stop button (first button) at the end of the list
        self.children = self.children[1:] + self.children[:1]
        # disable buttons that are unavailable to be pressed
        self._disable_unavailable_buttons()

    # To change the emoji or callback function, we can use the UI button decorator
    @nextcord.ui.button(emoji="\N{CROSS MARK}", label="Stop")
    async def stop_button(self, button, interaction):
        await interaction.response.send_message("You pressed stop.", ephemeral=True)
        self.stop()


class MySource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=6)

    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        return '\n'.join(f'{i}. {v}' for i, v in enumerate(entries, start=offset))


@bot.command()
async def pages(ctx):
    pages = CustomButtonMenuPages(source=MySource(range(1, 100)))
    await pages.start(ctx)


bot.run('token')
