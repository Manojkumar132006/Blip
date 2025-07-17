import socketio

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

socket_app = socketio.ASGIApp(sio)

@sio.event("connect")
async def connect(sid, environ):
    print(f"Client {sid} connected")
    await sio.emit("message", {"data": "Welcome!"}, room=sid)