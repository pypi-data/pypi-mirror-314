from trollbot.headers import URL, HEADERS
from trollbot.context import MessageContext
from trollbot.user import User
import socketio

class Bot:
    def __init__(self, name, color, prefix, verbose=True):
        self.socket = socketio.Client()

        self.name = name
        self.color = color
        self.prefix = prefix

        self.verbose = verbose

        blankfunc = (lambda *args: None)
        self.eventbindings = {
            "ready": blankfunc,
            "disconnect": blankfunc,
            "message": self.process_commands
        }

        self.commandbindings = {}
        self.unknownbinding = blankfunc

        self.rawuserlist = {}

        ############################################ SOCKETIO EVENTS SHIT
        # TODO: unshittify
        @self.socket.on("connect")
        def connect():
            self.socket.emit("user joined", (self.name, self.color, "", ""))
            if self.verbose: print("Connected to server")

        @self.socket.on("_connected")
        def _connected():
            self.eventbindings["ready"]()
            if self.verbose: print("Joined atrium")

        @self.socket.on("message")
        def message(data):
            self.eventbindings["message"](data)

        @self.socket.on("update users")
        def update_users(data):
            if self.verbose: print("User list updated")
            self.rawuserlist = data
            # print(self.rawuserlist)
        ############################################

    ############################# INTERAL FUNCTIONS

    def process_commands(self, data):
        if data["nick"] == self.name or not data["msg"].startswith(self.prefix):
            return
        
        tokens = data["msg"].split(" ")
        args = tokens[1:] if len(tokens) > 0 else []
        cmd = "".join(tokens[0].split(self.prefix))
        context = MessageContext(data, self)

        try:
            cmdfunc = self.commandbindings[cmd]
        except KeyError:
            self.unknownbinding(context, cmd)
        
        try:
            cmdfunc(context, *args)
        except TypeError as e:
            cmdfunc.errorfunc(context, e)

    ############################# 


    ############################# DECORATORS
    def event(self, event_name):
        def wrapper(func):
            self.eventbindings[event_name] = func

        return wrapper
    
    def command(self):
        def wrapper(func):
            self.commandbindings[func.__name__] = func

        return wrapper
    
    def unknown_command(self, func):
        self.unknownbinding = func

    def error(self, cmdname):
        # This one generates a decorator for commands

        def wrapper(func):
            self.commandbindings[cmdname].errorfunc = func

        return wrapper


    #############################


    ############################# REGULAR FUNCTIONS

    def send(self, message):
        self.socket.send(message)

    def getUsers(self):
        return [User(s, d, self) for s,d in self.rawuserlist.items()]
    
    def getUser(self, home):
        for sid, data in self.rawuserlist.items():
            if data["home"] == home:
                return User(sid, data, self)
    
    def connect(self, url=URL, headers=HEADERS, blocking=True):
        self.socket.connect(URL, headers=HEADERS)
        if blocking: self.socket.wait()

    #############################