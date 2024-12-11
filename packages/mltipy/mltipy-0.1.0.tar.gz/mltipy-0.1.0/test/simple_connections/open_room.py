import src.multipy as multipy
import asyncio

async def main():
    reciever = multipy.Client(open('./test/simple_connections/.env'))
    reciever.set_username('Reciever')
    await reciever.activate()
    room_id = await reciever.create_room()
    print(room_id)

    sender = multipy.Client(open('./test/simple_connections/.env'))
    sender.set_username('Sender')
    await sender.activate()
    await sender.join_room(room_id)
    
    reciever.add_event_hook("msg", lambda payload: print(payload))

    @reciever.on_event("msg")
    def log_msg(msg):
        print(f"{msg["username"]} sent: {msg["msg"]}")
    
    reciever.listen()
    
    sender.listen()
    print("Sending Event!")
    await asyncio.sleep(3)
    await sender.send_event("msg", {'username': sender.get_username(), "msg": "Hello!"})
    
    print("Waiting")
    await asyncio.sleep(3)
    
    del reciever
    del sender


if __name__ == '__main__':
    asyncio.run(main())
