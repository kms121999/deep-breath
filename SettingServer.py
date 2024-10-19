import asyncio
import websockets
import pickle
import threading

class SettingServer:
    def __init__(self, setting_manager, host='localhost', port=8765):
        self.setting_manager = setting_manager
        self.host = host
        self.port = port
        self.loop = None
        self.server = None

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

    async def start_server(self):
        """
        Start the WebSocket server and run until it's stopped.
        """
        self.server = await websockets.serve(self.handler, self.host, self.port)
        print(f"WebSocket server running on ws://{self.host}:{self.port}")

        # Keep the server running until it's stopped
        await self.server.wait_closed()

    def run_async_loop(self):
        """
        Run the asyncio event loop in a background thread.
        """
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # Run the WebSocket server in the loop
        self.loop.run_until_complete(self.start_server())
        self.loop.run_forever()

    def start(self):
        """
        Start the asyncio event loop and server in a separate thread.
        """
        self.thread = threading.Thread(target=self.run_async_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """
        Stop the WebSocket server and event loop.
        """
        if self.loop and self.server:
            # Close the WebSocket server
            self.loop.call_soon_threadsafe(self.server.close)

            # Stop the asyncio event loop
            self.loop.call_soon_threadsafe(self.loop.stop)

            # Wait for the thread to finish
            self.thread.join()


# Example usage
if __name__ == "__main__":
    import SettingManager  # Assuming SettingManager is defined elsewhere

    # Create the SettingServer instance
    setting_manager = SettingManager.SettingManager()
    ws_server = SettingServer(setting_manager, host="localhost", port=8765)

    # Start the WebSocket server in a separate thread
    ws_server.start()
    print("Server started in a background thread.")

    try:
        # Main thread can do other things here (e.g., running a GUI)
        while True:
            pass  # Replace this with actual main thread logic, like a Tkinter event loop
    except KeyboardInterrupt:
        print("Stopping server...")
        ws_server.stop()
        print("Server stopped gracefully.")
