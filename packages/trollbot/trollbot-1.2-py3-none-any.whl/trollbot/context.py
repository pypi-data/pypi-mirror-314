from trollbot.user import User

class MessageContext:
    def __init__(self, raw, bot):
        self.bot = bot

        self.date = raw["date"]
        self.user = next(self.bot.getUsers(home=raw["home"], nick=raw["nick"]))
        # self.color = raw["color"]
        # self.home = raw["home"]
        # self.style = raw["style"]
        # self.author = raw["nick"]