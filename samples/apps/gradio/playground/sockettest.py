import asyncio
import json
import websockets

# Replace with the actual URL of your websocket endpoint
websocket_url = "ws://localhost:8000/ws/140609438577184"  # Update client_id

async def send_message(message):
    async with websockets.connect(websocket_url) as websocket:
        try:
            await websocket.send(json.dumps(message))
            response = await websocket.recv()
            print(f"Server response: {response}")
        except Exception as e:  # Catch any exceptions during connection or message exchange
            print(f"Connection error: {e}")

async def main():
    # Example message to send
    message = {"type": "user_message", "data": {"message": "Hello from client!"}}
    await send_message(message)

if __name__ == "__main__":
    asyncio.run(main())
