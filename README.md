# Serpent Of Discord
A Python wrapper around the Discord API

```
from SODClient import SODClient

c = SODClient("email", "password")
c.login()

#Send a message to a channel you are a part of
c.sendMessage("server name","text channel name", "message")

c.logout()
```
