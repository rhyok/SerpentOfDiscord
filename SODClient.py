from SODAPIRequest import SODAPIRequest
from SODWebSocketClient import SODWebSocketClient
from threading import Thread

class SocketClientThread(Thread):
    def __init__(self, wsc):
        self.wsc = wsc
        Thread.__init__(self)

    def run(self):
        self.wsc.startConnection()

class SODClient:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.webSocketClient = None

    def login(self):
        """
        Logs you into Discord. Sets the authorization token
        """
        loginRequest = SODAPIRequest.LoginRequest(self.email, self.password)
        response = loginRequest.makeFormRequest()
        self.token = response["token"]

        gatewayRequest = SODAPIRequest("gateway", "GET", {"authorization": self.token}, {})
        response = gatewayRequest.makeRequest()
        gateway = response["url"]

        self.webSocketClient = SODWebSocketClient(self.token, gateway)

        self.socketClientThread = SocketClientThread(self.webSocketClient)
        try:
            self.socketClientThread.start()
        except KeyboardInterrupt:
            pass
        print "test"

    def logout(self):
        """
        Logs you out. Invalidates authorization token.
        """
        logoutRequest = SODAPIRequest.LogoutRequest(self.token)
        logoutRequest.makeRequest()
        self.token = None

    def sendMessage(self, guildName, channelName, message):
        cid = self.getTextChannelIDInGuildNamed(channelName, guildName)
        if cid is not None:
            self.sendMessageWithId(cid, message)
        else:
            # Should raise exception here instead
            print "I cannot do it :<"

    def getMessages(self):
        return self.webSocketClient.getMessages()

    def sendMessageWithId(self, channelId, message):
        sendMessageRequest = SODAPIRequest.SendMessageRequest(self.token, channelId, message)
        sendMessageRequest.makeRequest()

    def getTextChannelIDInGuildNamed(self, channelName, guildName):
        guilds = SODAPIRequest.GuildsRequest(self.token).makeRequest()
        guildId = None
        for guild in guilds:
            name = guild.get("name")
            if name == guildName:
                guildId = guild.get("id")

        if guildId is not None:
            channels = SODAPIRequest.ChannelsRequest(self.token, guildId).makeRequest()
            for channel in channels:
                if channel.get("name") == channelName and channel.get("type") == "text":
                    return channel.get("id")
        return None
