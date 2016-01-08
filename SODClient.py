from SODAPIRequest import SODAPIRequest


class SODClient:
    """
    A client for Discord, a chat application.
    """
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def login(self):
        """
        Logs you into Discord. Sets the authorization token
        """
        loginRequest = SODAPIRequest.LoginRequest(self.email, self.password)
        response = loginRequest.makeFormRequest()
        self.token = response["token"]

    def logout(self):
        """
        Logs you out. Invalidates authorization token.
        """
        logoutRequest = SODAPIRequest.LogoutRequest()
        logoutRequest.makeRequest()
        self.token = None

    def sendMessage(self, guildName, channelName, message):
        cid = self.getTextChannelIDInGuildNamed(channelName, guildName)
        if cid is not None:
            self.sendMessageWithId(cid, message)
        else:
            # Should raise exception here instead
            print "I cannot do it :<"

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
