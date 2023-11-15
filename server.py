import asyncio

import uvicorn
from fastapi import FastAPI
from sse_starlette import EventSourceResponse
from starlette.responses import StreamingResponse


app = FastAPI()


async def mock_request():
    for i in range(5):
        yield (f"chunk {i}").encode()
        await asyncio.sleep(0.5)


@app.post("/stream")
async def stream():
    resp = mock_request()

    async def generator():
        async for d in resp:
            yield d.decode()

    return StreamingResponse(
        generator(),
        media_type="text/event-stream",
    )


@app.post("/sse")
async def sse():
    resp = mock_request()

    async def generator():
        async for d in resp:
            yield {"data": d.decode()}

    return EventSourceResponse(generator())


if __name__ == "__main__":
    uvicorn.run(app, port=5001)
