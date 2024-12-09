from trollbot.user import User

class MessageContext:
    def __init__(self, raw, bot):
        self.bot = bot

        self.date = raw["date"]
        self.user = self.bot.getUser(raw["home"])
        # self.color = raw["color"]
        # self.home = raw["home"]
        # self.style = raw["style"]
        # self.author = raw["nick"]