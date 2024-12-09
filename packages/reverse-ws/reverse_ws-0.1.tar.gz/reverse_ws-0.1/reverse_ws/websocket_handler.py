import asyncio
import websockets

async def connect_reverse_websocket():
    uri = "ws://localhost:8765"  # Adresse du serveur WebSocket
    try:
        async with websockets.connect(uri) as websocket:
            print("WebSocket connection established.")
            await websocket.send("Client connected.")
            # Gérer les messages ici
            while True:
                response = await websocket.recv()
                print(f"Message from server: {response}")
    except Exception as e:
        print(f"Error in WebSocket connection: {e}")

def start_websocket_client():
    asyncio.run(connect_reverse_websocket())
