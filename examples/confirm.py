import nextcord
from nextcord.ext import commands, menus


bot = commands.Bot(command_prefix="$")


class ButtonConfirm(menus.ButtonMenu):
    def __init__(self, text):
        super().__init__(timeout=15.0, delete_message_after=True)
        self.text = text
        self.result = None

    async def send_initial_message(self, ctx, channel):
        return await channel.send(self.text, view=self)

    @nextcord.ui.button(emoji='\N{WHITE HEAVY CHECK MARK}')
    async def do_confirm(self, button, interaction):
        self.result = True
        self.stop()

    @nextcord.ui.button(emoji='\N{CROSS MARK}')
    async def do_deny(self, button, interaction):
        self.result = False
        self.stop()

    async def prompt(self, ctx):
        await menus.Menu.start(self, ctx, wait=True)
        return self.result


@bot.command()
async def confirm(ctx):
    answer = await ButtonConfirm('Confirm?').prompt(ctx)
    await ctx.send(f'You said: {answer}')


bot.run('token')
