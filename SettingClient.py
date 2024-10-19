import asyncio
from websockets.sync.client import connect
import pickle

class SettingClient:
    def __init__(self):
        self.uri = "ws://localhost:8765"

    def get_settings(self, callback):
        """
        This function will be used to get the settings from the server.
        """
        self._request({"command": "getSettings"}, callback)

    def set_settings(self, settings, callback):
        """
        This function will be used to set the settings on the server.
        """
        def wrapped_callback(result, error=None):
            if error:
                callback(False, error)
            elif result.get("status") == "success":
                callback(True)
            else:
                callback(False, result.get("error"))

        self._request({"command": "setSettings", "data": settings}, wrapped_callback)

    def _request(self, payload, callback):
        with connect(self.uri) as websocket:
            print("Connected to WebSocket server!")

            # Serialize (pickle) the message object
            serialized_message = pickle.dumps(payload)

            # Send the serialized object to the server
            print(f"Sending object: {payload}")
            websocket.send(serialized_message)

            # Receive and deserialize the response from the server
            try:
                serialized_response = websocket.recv()
                response_object = pickle.loads(serialized_response)
                
                print(f"Received object from server: {response_object}")
                callback(response_object)
            except Exception as e:
                callback(None, e)

# Example usage
if __name__ == "__main__":
    def set_settings_callback(status, error = None):
        if status:
            print("Settings updated successfully!")
        else:
            print(f"Failed to update settings: {error}")

    def get_settings_callback(settings, error = None):
        print(f"Received settings: {settings}")
        settings['color'] = 'pink'
        client.set_settings(settings, set_settings_callback)
    client = SettingClient()
    client.get_settings(get_settings_callback)
    asyncio.get_event_loop().run_forever()
    # asyncio.get_event_loop().run_until_complete()

