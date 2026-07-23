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


class StreamerSession:
    """Una sesión = un streamer + todos los usuarios de la app viéndolo."""
    def __init__(self, username: str):
        self.username = username
        self.subscribers: list[WebSocket] = []
        self.client: TikTokLiveClient | None = None
        self.task: asyncio.Task | None = None

    async def broadcast(self, data: dict):
        dead = []
        for ws in self.subscribers:
            try:
                await ws.send_text(json.dumps(data))
            except Exception:
                dead.append(ws)
        for d in dead:
            if d in self.subscribers:
                self.subscribers.remove(d)

    async def start(self):
        client = TikTokLiveClient(unique_id=self.username)

        @client.on(ConnectEvent)
        async def on_connect(event: ConnectEvent):
            await self.broadcast({"type": "status", "status": "connected", "user": self.username})

        @client.on(DisconnectEvent)
        async def on_disconnect(event: DisconnectEvent):
            await self.broadcast({"type": "status", "status": "disconnected"})

        @client.on(CommentEvent)
        async def on_comment(event: CommentEvent):
            await self.broadcast({"type": "comment", "user": event.user.nickname, "comment": event.comment})

        @client.on(GiftEvent)
        async def on_gift(event: GiftEvent):
            if not event.gift.streakable or event.repeat_end:
                await self.broadcast({
                    "type": "gift", "user": event.user.nickname,
                    "gift": event.gift.name, "count": event.repeat_count
                })

        @client.on(LikeEvent)
        async def on_like(event: LikeEvent):
            await self.broadcast({"type": "like", "user": event.user.nickname, "count": event.count})

        @client.on(FollowEvent)
        async def on_follow(event: FollowEvent):
            await self.broadcast({"type": "follow", "user": event.user.nickname})

        self.client = client
        try:
            await client.start()
        except UserOfflineError:
            await self.broadcast({"type": "status", "status": "error", "message": "user_offline"})
        except UserNotFoundError:
            await self.broadcast({"type": "status", "status": "error", "message": "user_not_found"})
        except Exception as e:
            logger.exception(f"Error en sesión de @{self.username}")
            await self.broadcast({"type": "status", "status": "error", "message": str(e)})
        finally:
            sessions.pop(self.username, None)

    def stop(self):
        if self.client:
            asyncio.create_task(self.client.disconnect())
        if self.task:
            self.task.cancel()


# username -> StreamerSession
sessions: dict[str, StreamerSession] = {}
sessions_lock = asyncio.Lock()


@app.get("/")
def root():
    return {"status": "ok", "active_streamers": list(sessions.keys())}


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    username = username.strip().lower()
    await websocket.accept()

    async with sessions_lock:
        session = sessions.get(username)
        if session is None:
            session = StreamerSession(username)
            sessions[username] = session
            session.task = asyncio.create_task(session.start())
        session.subscribers.append(websocket)

    logger.info(f"Usuario conectado viendo @{username} ({len(session.subscribers)} viendo)")

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        session.subscribers.remove(websocket)
        logger.info(f"Usuario se fue de @{username} ({len(session.subscribers)} restantes)")

        # Si ya nadie está viendo a este streamer, cerramos la conexión con TikTok
        if not session.subscribers:
            async with sessions_lock:
                if username in sessions and not sessions[username].subscribers:
                    sessions[username].stop()
                    sessions.pop(username, None)
                    logger.info(f"Cerrada la sesión de @{username}, nadie la está viendo")
