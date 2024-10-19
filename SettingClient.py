import asyncio
import websockets
import pickle

class SettingClient:
    def __init__(self):
        self.uri = "ws://localhost:8765"

    async def get_settings(self, callback):
        """
        This function will be used to get the settings from the server.
        """
        await self._request({"command": "getSettings"}, callback)

    async def set_settings(self, settings, callback):
        """
        This function will be used to set the settings on the server.
        """
        def wrapped_callback(result, error=None):
            if error:
                callback(False, error)
            elif result.get("status") == "success":
                callback(True)
            else:
                callback(False, None)

        await self._request({"command": "setSettings", "data": settings}, wrapped_callback)

    async def _request(self, payload, callback):
        async with websockets.connect(self.uri) as websocket:
            print("Connected to WebSocket server!")

            # Serialize (pickle) the message object
            serialized_message = pickle.dumps(payload)

            # Send the serialized object to the server
            print(f"Sending object: {payload}")
            await websocket.send(serialized_message)

            # Receive and deserialize the response from the server
            try:
                serialized_response = await websocket.recv()
                response_object = pickle.loads(serialized_response)

                print(f"Received object from server: {response_object}")
                callback(response_object)
            except Exception as e:
                callback(None, e)




if __name__ == "__main__":
    color = input("New color: ")
    async def main():
        client = SettingClient()
        settings = {}

        def set_settings_callback(status, error=None):
            if status:
                print("Settings updated successfully!")
            else:
                print(f"Failed to update settings: {error}")

        def get_settings_callback(received, error=None):
            print(f"Received settings: {received}")
            global settings
            settings = received

        await client.get_settings(get_settings_callback)
        settings['color'] = color
        await client.set_settings(settings, set_settings_callback)


    asyncio.run(main())
