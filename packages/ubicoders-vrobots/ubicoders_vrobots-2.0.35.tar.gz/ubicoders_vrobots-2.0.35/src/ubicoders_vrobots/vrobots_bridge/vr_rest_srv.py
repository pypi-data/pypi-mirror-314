from fastapi import FastAPI
import uvicorn
import websockets
from fastapi.middleware.cors import CORSMiddleware
import asyncio  # Import asyncio


async def check_alive(uri):
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(b"ping")
            response = await websocket.recv()
            return response == b"pong"
    except websockets.exceptions.ConnectionClosed:
        return False


def create_app():
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins, replace with your specific origins in production
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    @app.get("/")
    async def default():
        return "ok"

    @app.get("/ping")
    async def ping():
        return {"status": 1, "data": None, "msg": "ok"}
    return app


async def run_rest_server(port=12741):
    app = create_app()
    config = uvicorn.Config(
        app=app, host="0.0.0.0", port=port, loop="asyncio", log_level="warning"
    )
    server = uvicorn.Server(config)
    print(f"\033[92mVirtual Robots REST Bridge is running @ port {port}\033[0m")
    await server.serve()


if __name__ == "__main__":
    try:
        asyncio.run(run_rest_server())
    except KeyboardInterrupt:
        print("Server stopped by user.")
