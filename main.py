import asyncio
import json
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from TikTokLive import TikTokLiveClient
from TikTokLive.client.errors import UserOfflineError, UserNotFoundError
from TikTokLive.events import CommentEvent, ConnectEvent, DisconnectEvent, GiftEvent, LikeEvent, FollowEvent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tiktok-tts")

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, data: dict):
        dead = []
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(data))
            except Exception:
                dead.append(connection)
        for d in dead:
            self.disconnect(d)

manager = ConnectionManager()

tiktok_client: TikTokLiveClient | None = None
tiktok_task: asyncio.Task | None = None
connection_lock = asyncio.Lock()  # 👈 evita pisar conexiones a medias


async def start_tiktok_client(username: str):
    global tiktok_client
    client = TikTokLiveClient(unique_id=username)

    @client.on(ConnectEvent)
    async def on_connect(event: ConnectEvent):
        logger.info(f"Conectado al live de @{username}")
        await manager.broadcast({"type": "status", "status": "connected", "user": username})

    @client.on(DisconnectEvent)
    async def on_disconnect(event: DisconnectEvent):
        logger.info("Desconectado del live")
        await manager.broadcast({"type": "status", "status": "disconnected"})

    @client.on(CommentEvent)
    async def on_comment(event: CommentEvent):
        await manager.broadcast({"type": "comment", "user": event.user.nickname, "comment": event.comment})

    @client.on(GiftEvent)
    async def on_gift(event: GiftEvent):
        if not event.gift.streakable or event.repeat_end:
            await manager.broadcast({
                "type": "gift", "user": event.user.nickname,
                "gift": event.gift.name, "count": event.repeat_count
            })

    @client.on(LikeEvent)
    async def on_like(event: LikeEvent):
        await manager.broadcast({"type": "like", "user": event.user.nickname, "count": event.count})

    @client.on(FollowEvent)
    async def on_follow(event: FollowEvent):
        await manager.broadcast({"type": "follow", "user": event.user.nickname})

    tiktok_client = client

    try:
        await client.start()
    except UserOfflineError:
        logger.warning(f"@{username} no está en vivo ahorita")
        await manager.broadcast({"type": "status", "status": "error", "message": "user_offline"})
    except UserNotFoundError:
        logger.warning(f"@{username} no existe")
        await manager.broadcast({"type": "status", "status": "error", "message": "user_not_found"})
    except Exception as e:
        logger.exception("Error inesperado conectando a TikTok")
        await manager.broadcast({"type": "status", "status": "error", "message": str(e)})
    finally:
        tiktok_client = None


@app.get("/")
def root():
    return {"status": "ok", "message": "TikTok TTS backend corriendo"}


@app.post("/connect/{username}")
async def connect_to_tiktok(username: str):
    global tiktok_task
    async with connection_lock:
        if tiktok_task and not tiktok_task.done():
            return {"error": "Ya hay una conexión activa. Desconéctala primero."}
        tiktok_task = asyncio.create_task(start_tiktok_client(username))
    return {"status": "conectando", "user": username}


@app.post("/disconnect")
async def disconnect_from_tiktok():
    global tiktok_client, tiktok_task
    async with connection_lock:
        if tiktok_client:
            await tiktok_client.disconnect()
            tiktok_client = None
        if tiktok_task:
            tiktok_task.cancel()
            tiktok_task = None
    return {"status": "desconectado"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
