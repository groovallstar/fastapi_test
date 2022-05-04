from aioredis import Channel, Redis
from fastapi import FastAPI
from fastapi.params import Depends
from fastapi_plugins import depends_redis, redis_plugin
from sse_starlette.sse import EventSourceResponse
from starlette.responses import HTMLResponse

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>SSE</title>
    </head>
    <body>
        <script>
            const evtSource = new EventSource("http://localhost:8000/sse/stream");
            evtSource.addEventListener("message", function(event) {
                // Logic to handle status updates
                console.log(event.data)
            });  
        </script>
    </body>
</html>
"""


app = FastAPI()


@app.on_event("startup")
async def on_startup() -> None:
    await redis_plugin.init_app(app)
    await redis_plugin.init()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await redis_plugin.terminate()


@app.get("/sse/demo")
async def get():
    return HTMLResponse(html)


@app.get("/sse/publish")
async def get(channel: str = "default", redis: Redis = Depends(depends_redis)):
    await redis.publish(channel=channel, message="Hello world!")
    return ""


@app.get("/sse/stream")
async def stream(channel: str = "default", redis: Redis = Depends(depends_redis)):
    return EventSourceResponse(subscribe(channel, redis))


async def subscribe(channel: str, redis: Redis):
    (channel_subscription,) = await redis.subscribe(channel=Channel(channel, False))
    while await channel_subscription.wait_message():
        yield {"event": "message", "data": await channel_subscription.get()}
