from Tracker import Tracker

from setting_management.SettingServer import SettingServer
from setting_management.SettingManager import SettingManager

def main():
    print("booting up...")
    # Create the SettingServer instance
    setting_manager = SettingManager()
    ws_server = SettingServer(setting_manager, host="localhost", port=8765)

    # Start the WebSocket server in a separate thread
    ws_server.start()
    print("Server started in a background thread.")

    try:
        # Initiate the tracker 
        running_Tracker = Tracker()
        # Start the 1 minute tick
        running_Tracker.tick()
    finally:
        print("Stopping server...")
        ws_server.stop()
        print("Server stopped gracefully.")

if __name__ == '__main__':
    main()