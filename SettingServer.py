import asyncio
import websockets
import pickle
import threading

class SettingServer(threading.Thread):
    def __init__(self, setting_manager, host='localhost', port=8765):
        super().__init__()

        self.setting_manager = setting_manager

        self.host = host
        self.port = port

        # Cite https://stackoverflow.com/a/57627601/7865238
        self.stop_event = threading.Event()


    async def handler(self, websocket, path):
        """
        Handler that manages the connection and communication.
        """
        print(f"Client connected from {websocket.remote_address}")

        try:
            async for received_data in websocket:
                # Deserialize (unpickle) the received message
                payload = pickle.loads(received_data)
                print(f"Received object from client: {payload}")

                response_data = None

                match payload["command"]:
                    case "getSettings":
                        # Get the settings from the SettingManager
                        response_data = self.setting_manager.get_settings()
                    case "setSettings":
                        # Set the settings in the SettingManager
                        self.setting_manager.set_settings(payload["data"])
                        response_data = {"status": "success"}

                
                # Serialize (pickle) the response
                serialized_response = pickle.dumps(response_data)
                
                # Send the serialized response back to the client
                await websocket.send(serialized_response)
                print(f"Sent object to client: {response_data}")
                
        except websockets.ConnectionClosedOK:
            print("Client disconnected gracefully.")
        except websockets.ConnectionClosedError as e:
            print(f"Connection closed with error: {e}")
        except KeyError as e:
            print(f"Invalid command received: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def run(self):
        """
        Start the WebSocket server.
        """
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # Start the WebSocket server
        self.serve = websockets.serve(self.handler, self.host, self.port)
        print(f"WebSocket server running on {self.host}:{self.port}")

        # asyncio.get_event_loop().run_in_executor(None, self.stop_event.wait)

        self.loop.run_until_complete(self.serve)
        self.loop.run_forever()

    def stop(self):
        """
        Stop the WebSocket server.
        """
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.stop_event.set()

# Example usage
if __name__ == "__main__":
    import SettingManager
    ws_server = SettingServer(SettingManager.SettingManager(), host="localhost", port=8765)
    ws_server.start()
    print("Server Started")

    try:
        while True:
            pass
    finally:
        ws_server.stop()
        ws_server.join()
        print("Server Stopped Gracefully")
