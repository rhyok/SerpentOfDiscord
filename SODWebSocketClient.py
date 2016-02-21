from ws4py.client.threadedclient import WebSocketClient
from ModuLog import ModuLog
from threading import Timer, Thread, Event
import json
import time

class HeartbeatThread(Thread):
    def __init__(self, stopEvent, heartbeatTime, client):
        Thread.__init__(self)
        self.stopEvent = stopEvent

    def run(self):
        while not self.stopEvent.wait(self.heartbeatTime):
            self.client.sendHeartbeat()


class SODWebSocketClient(WebSocketClient):
    def __init__(self, apiToken, gateway):
        self.messageQueue = []
        self.apiToken = apiToken
        self.stopHeartbeat = None
        WebSocketClient.__init__(self, gateway)
        self.heartbeat_freq = 2.0

    def opened(self):
        #connection was opened
        ModuLog.info("WSC", "Connection opened")
        self.sendConnectionStartMessage()

    def closed(self, code, reason):
        ModuLog.info("WSC", "Connection closed")

    def received_message(self, message):
        if(message.is_text):
            ModuLog.info("WSC", "New message received: " + message.data)
            message = json.loads(message.data)
            if(message["t"] == "READY"):
                stopHeartbeat = Event()
                interval = float(message["t"]["d"]["heartbeat_interval"])/1000
                heartbeatThread = HeartbeatThread(stopHeartbeat, interval, self)
                try:
                    heartbeatThread.start()
                except KeyboardInterrupt:
                    pass

            self.messageQueue.append(message)

    def getMessages(self):
        messages = list(self.messageQueue)
        self.messageQueue = []
        return messages

    def startConnection(self):
        try:
            self.connect()
            self.run_forever()
        except KeyboardInterrupt:
            self.close()

    def sendConnectionStartMessage(self):
        startMessage = """
        {{
        "op": 2,
        "d": {{
                "token": "{0}",
                "v": 3,
                "properties": {{
                        "$os": "Windows",
                        "$browser": "Chrome",
                        "$device": "",
                        "$referrer":" https://discordapp.com/@me",
                        "$referring_domain":"discordapp.com"
                }},
                "large_threshold":100,
                "compress":true
            }}
        }}
        """
        startMessage = str.format(startMessage, self.apiToken)
        self.send(startMessage)

    def sendHeartbeat(self):
        message = """
        {{
            "op": 1,
            "d": {0}
        }}
        """
        message = str.format(message, int(time.time()*1000))
        self.send(message)
