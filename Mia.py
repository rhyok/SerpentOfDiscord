from SODClient import SODClient

client = SODClient("experimentpants@gmail.com", "test123")

client.login()

running = True
while(running):
    newMessages = client.getMessages()

    for message in newMessages:
        if(message["t"] == "MESSAGE_CREATE" and message["d"]["author"]["username"] != "Mia"):
            print "*****\nEchoing\n*****"
            channel = message["d"]["channel_id"]
            client.sendMessageWithId(channel, message["d"]["content"])
