import nextcord
from nextcord.ext import commands, menus


bot = commands.Bot(command_prefix="$")


class CustomButtonMenuPages(menus.ButtonMenuPages, inherit_buttons=False):
    """
    This class overrides the default ButtonMenuPages without inheriting the buttons
    by setting inherit_buttons to False.

    This allows us to add our own buttons with custom labels, styles, or even callbacks. 
    """

    def __init__(self, source, timeout=60):
        super().__init__(source, timeout=timeout)
        
        # You can change the buttons to have custom labels and styles by setting
        # inherit_buttons=False above and adding them with self.add_item as shown below.
        # Note: None of the buttons are required you can leave any of them out
        self.add_item(menus.MenuPaginationButton(emoji=self.FIRST_PAGE, label="First"))
        self.add_item(menus.MenuPaginationButton(emoji=self.PREVIOUS_PAGE, label="Prev"))
        self.add_item(menus.MenuPaginationButton(emoji=self.NEXT_PAGE, label="Next"))
        self.add_item(menus.MenuPaginationButton(emoji=self.LAST_PAGE, label="Last"))
        
        # Rearrange the buttons (place the Stop button (first button) at the end of the list)
        self.children = self.children[1:] + self.children[:1]
        
        # Disable buttons that are unavailable to be pressed at the start
        self._disable_unavailable_buttons()

    # To change the callback function, we can use the button decorator
    @nextcord.ui.button(emoji="\N{BLACK SQUARE FOR STOP}", label="Stop")
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
    data = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    pages = CustomButtonMenuPages(source=MySource(data))
    await pages.start(ctx)


bot.run('token')
