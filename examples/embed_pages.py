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
        embed.set_footer(text=f"Page {menu.current_page + 1}/{self.get_max_pages()}")
        return embed


@bot.command()
async def button_embed_field(ctx):
    data = [
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
        source=MyEmbedFieldPageSource(data),
        clear_buttons_after=True,
    )
    await pages.start(ctx)


@bot.command()
async def reaction_embed_field(ctx):
    data = [
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
    pages = menus.MenuPages(
        source=MyEmbedFieldPageSource(data),
        clear_reactions_after=True,
    )
    await pages.start(ctx)


class MyEmbedDescriptionPageSource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=6)

    async def format_page(self, menu, entries):
        embed = Embed(title="Entries", description="\n".join(entries))
        embed.set_footer(text=f"Page {menu.current_page + 1}/{self.get_max_pages()}")
        return embed


@bot.command()
async def button_embed_description(ctx):
    data = [f"Description for entry #{num}" for num in range(1, 51)]
    pages = menus.ButtonMenuPages(
        source=MyEmbedDescriptionPageSource(data),
        clear_buttons_after=True,
    )
    await pages.start(ctx)


bot.run("token")
