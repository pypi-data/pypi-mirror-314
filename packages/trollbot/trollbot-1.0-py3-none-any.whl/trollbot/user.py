class User:
    def __init__(self, sid, raw, bot):
        self.raw = raw
        self.sid = sid
        self.bot = bot 

        self.nick = raw["nick"]
        self.room = raw["room"]
        self.home = raw["home"]
        self.color = raw["color"]
        self.style = raw["style"]
        self.isbot = raw["isBot"]