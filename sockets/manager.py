"""
Socket.IO Manager with Rooms and Access Control
"""
import socketio
from fastapi import Request
from utils.auth import verify_token, TokenData
from config.database import db

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")

# In-memory session store (use Redis in production)
connected_users = {}  # sid -> user_id
user_rooms = {}       # user_id -> set of rooms

@sio.event
async def connect(sid, environ):
    try:
        # Extract token
        query = environ.get("QUERY_STRING", "")
        if "token=" not in query:
            await sio.disconnect(sid)
            return False
        token = query.split("token=")[1].split("&")[0]
        user = verify_token(token)
        if not user:
            await sio.disconnect(sid)
            return False

        # Attach user
        sio.user_id = user.user_id
        connected_users[sid] = user.user_id
        user_rooms.setdefault(user.user_id, set())

        print(f"User {user.user_id} connected via Socket.IO")
        await sio.emit("connected", {"message": "Authenticated and connected"}, room=sid)
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        await sio.disconnect(sid)
        return False

@sio.event
async def disconnect(sid):
    user_id = connected_users.pop(sid, None)
    if user_id:
        rooms = user_rooms.get(user_id, set())
        for room in rooms:
            await sio.leave_room(sid, room)
        user_rooms.pop(user_id, None)
    print(f"User {user_id} disconnected")

@sio.event
async def join_cluster(sid, data):
    cluster_id = data.get("cluster_id")
    if not cluster_id:
        await sio.emit("error", {"message": "cluster_id required"}, room=sid)
        return

    # Verify user belongs to cluster
    user_id = connected_users.get(sid)
    user = db.users.find_one({"_id": user_id})
    if not user or str(user.get("cluster_id")) != cluster_id:
        await sio.emit("error", {"message": "Access denied"}, room=sid)
        return

    await sio.enter_room(sid, f"cluster:{cluster_id}")
    user_rooms[user_id].add(f"cluster:{cluster_id}")
    await sio.emit("joined", {"room": f"cluster:{cluster_id}"}, room=sid)

@sio.event
async def create_spark(sid, data):
    user_id = connected_users.get(sid)
    if not user_id:
        return

    cluster_id = data.get("cluster_id")
    group_id = data.get("group_id", None)
    title = data.get("title")
    location = data.get("location")
    expires_at = data.get("expires_at")

    if not all([cluster_id, title, location, expires_at]):
        await sio.emit("error", {"message": "Missing required fields"}, room=sid)
        return

    # Validate user in cluster
    user = db.users.find_one({"_id": user_id})
    if not user or str(user.get("cluster_id")) != cluster_id:
        await sio.emit("error", {"message": "Unauthorized"}, room=sid)
        return

    # Create spark (minimal for demo)
    spark_data = {
        "creator_id": user_id,
        "cluster_id": cluster_id,
        "group_id": group_id,
        "title": title,
        "location": location,
        "expires_at": datetime.fromisoformat(expires_at),
        "current_participants": [user_id],
        "is_active": True,
        "created_at": datetime.utcnow()
    }
    result = db.sparks.insert_one(spark_data)
    spark_id = str(result.inserted_id)

    # Broadcast
    room = f"group:{group_id}" if group_id else f"cluster:{cluster_id}"
    await sio.emit("spark_created", {
        "spark_id": spark_id,
        "title": title,
        "creator_id": user_id,
        "location": location,
        "timestamp": spark_data["created_at"].isoformat()
    }, room=room)

@sio.event
async def match_request(sid, data):
    user_id = connected_users.get(sid)
    if not user_id:
        return

    # Placeholder matching logic
    # In practice: match based on routines + vibe (mood/energy from frontend)
    matches = []  # Simulated
    await sio.emit("match_result", {
        "user_id": user_id,
        "matches": matches,
        "message": "Matching logic placeholder — integrate time overlap + vibe algorithm"
    }, room=sid)

@sio.event
async def send_message(sid, data):
    user_id = connected_users.get(sid)
    if not user_id:
        return

    room_type = data.get("type")  # "group" or "spark"
    room_id = data.get("id")
    message = data.get("message")

    if not all([room_type, room_id, message]):
        await sio.emit("error", {"message": "Invalid message data"}, room=sid)
        return

    target_room = f"{room_type}:{room_id}"

    # Sanitize and emit
    safe_data = {
        "sender_id": user_id,
        "message": message[:500],  # limit length
        "timestamp": datetime.utcnow().isoformat(),
        "type": room_type
    }
    await sio.emit("new_message", safe_data, room=target_room)
