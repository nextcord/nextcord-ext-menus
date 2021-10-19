import nextcord
from nextcord.ext import commands, menus


bot = commands.Bot(command_prefix="$")


class CustomEmojiButtonMenuPages(menus.ButtonMenuPages):
    r"""
    This class overrides the default ButtonMenuPages replacing the emoji attributes

    Emojis can be specified in any of the following string formats:
    - <:name:id> for custom emojis
    - <a:name:id> for custom animated emojis
    - A string containing the unicode emoji's name in the format \N{name}
    - A string containing the unicode emoji character

    Note: for custom emojis to work, the emoji must be in a server that the bot is in.
    """

    FIRST_PAGE = "<:pagefirst:899973860772962344>"
    LAST_PAGE = "<:pagelast:899973860810694686>"
    PREVIOUS_PAGE = "\N{WHITE LEFT POINTING BACKHAND INDEX}"
    NEXT_PAGE = "\N{WHITE RIGHT POINTING BACKHAND INDEX}"
    STOP = "\N{OCTAGONAL SIGN}"


class MySource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=6)

    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        return '\n'.join(f'{i}. {v}' for i, v in enumerate(entries, start=offset))


@bot.command()
async def pages(ctx):
    pages = CustomEmojiButtonMenuPages(source=MySource(range(1, 100)))
    await pages.start(ctx)


bot.run('token')
