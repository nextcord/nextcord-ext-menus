from nextcord import Embed
from nextcord.ext import commands, menus


bot = commands.Bot(command_prefix="$")


class MyEmbedFieldPageSource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=2)

    async def format_page(self, menu, entries):
        embed = Embed(title="Entries")
        for entry in entries:
            embed.add_field(name=entry[0], value=entry[1], inline=True)
        embed.set_footer(text=f'Page {menu.current_page + 1}/{self.get_max_pages()}')
        return embed


@bot.command(aliases=["bef"])
async def button_embed_field(ctx):
    pages = menus.ButtonMenuPages(
        source=MyEmbedFieldPageSource(list(zip('abcdefghij', range(1, 11)))),
        clear_buttons_after=True,
    )
    await pages.start(ctx)


@bot.command(aliases=["ref"])
async def reaction_embed_field(ctx):
    pages = menus.MenuPages(
        source=MyEmbedFieldPageSource(list(zip('abcdefghij', range(1, 11)))),
        clear_reactions_after=True,
    )
    await pages.start(ctx)


class MyEmbedDescriptionPageSource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=6)

    async def format_page(self, menu, entries):
        embed = Embed(title="Entries", description="\n".join(entries))
        embed.set_footer(text=f'Page {menu.current_page + 1}/{self.get_max_pages()}')
        return embed


@bot.command(aliases=["bed"])
async def button_embed_description(ctx):
    data = [f'Description for entry #{num}' for num in range(1, 51)]
    pages = menus.ButtonMenuPages(
        source=MyEmbedDescriptionPageSource(data),
        clear_buttons_after=True,
    )
    await pages.start(ctx)


bot.run('token')
