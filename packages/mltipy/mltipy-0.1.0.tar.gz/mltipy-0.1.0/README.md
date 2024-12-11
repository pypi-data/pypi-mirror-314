# Multipy

Make multiplayer in Python simple!

## Quick Intro

### Install it

```shell
pip install realtime mltipy
```

### And use it

```py

import multipy

# Create a new client
# Initialize by passing the Project ID and key...
client = multipy.Client(("<PROJECT ID>", "<API KEY>"))

# ...Or use a `.env`
### .env ###
# PROJECT_ID=<PROJECT_ID>
# API_KEY=<API KEY>
client = multipy.Client(open("./.env"))

async def main():
    client.set_username('client1')
    await client.activate()

    await client.join_room('<ROOM NAME>')
    await client.listen()

    # Recieve some stuff..
    @client.on_event("msg")
    def on_msg(payload):
        print(payload)
    
    # Or send some!
    await client.send_event

    # Do Stuff...
    await client.terminate()
    # or use this
    -client
```
