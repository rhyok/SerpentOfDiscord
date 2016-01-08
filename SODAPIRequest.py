from httplib import HTTPSConnection
import httplib
import urllib
import json


class SODAPIRequestFailedException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class SODAPIRequest:
    """
    A convenience class for constructing API calls to Discord.
    Also has templates for a few of the common API calls.
    """

    SODDiscordServerAddress = "discordapp.com"
    SODDiscordAPIPrefix = "/api/"
    SODStandardFormHeaders = {"Content-type": "application/x-www-form-urlencoded",
                              "Accept": "*/*"}

    def __init__(self, apiEndpoint, method, headers, body):
        """
        General constructor.

        apiEndpoint (string): the API endpoint you want to make a request to.
        Should be the part of the url after "https://discordapp.com/api/"

        method (string): the HTTP method you want to use ("POST" or "GET")

        parameters (dict): a dictionary of parameters.
        """
        self.endpoint = SODAPIRequest.SODDiscordAPIPrefix + apiEndpoint
        self.method = method
        self.headers = headers
        self.body = body

    def makeFormRequest(self):
        self.body = urllib.urlencode(self.body)
        return self.makeRequest()

    def makeRequest(self):
        """
        Makes the request you have specified and returns the response
        as a dict.

        If the request does not return 200 OK, it raises a SODAPIRequestFailedException instead

        token - Authorization token
        """
        try:
            conn = HTTPSConnection(SODAPIRequest.SODDiscordServerAddress)
            conn.request(self.method, self.endpoint, self.body, self.headers)
            response = conn.getresponse()
            if response.status == httplib.OK:
                return json.loads(response.read())
            else:
                raise SODAPIRequestFailedException("Response was: " + str(response.status) + " " + response.reason)
        except Exception as e:
            #TODO: Logging.
            raise e

    # Template requests
    @staticmethod
    def LoginRequest(email, password):
        return SODAPIRequest("auth/login", "POST", SODAPIRequest.SODStandardFormHeaders, {"email": email, "password": password})

    @staticmethod
    def LogoutRequest(token):
        return SODAPIRequest("auth/logout", "POST", SODAPIRequest.SODStandardFormHeaders, {})

    @staticmethod
    def SendMessageRequest(token, channelId, content):
        return SODAPIRequest("channels/" + channelId + "/messages", "POST", {"authorization": token, "Content-Type": "application/json"}, json.dumps({"content": content}))

    @staticmethod
    def GuildsRequest(token):
        return SODAPIRequest("users/@me/guilds", "GET", {"authorization": token}, {})

    @staticmethod
    def ChannelsRequest(token, guildId):
        return SODAPIRequest("guilds/" + str(guildId) + "/channels", "GET", {"authorization": token}, {})
