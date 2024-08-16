import NHCManager

from config import *


def main():
    # Create a new NHC Manager.
    nhc = NHCManager.Manager()

    # Connect to the server
    nhc.connect(ADDRESS, PORT, USERNAME, PASSWORD, CERTIFICATE)

    # Start the connection (non-blocking).
    nhc.start()

    # Collect all devices (actions) and their properties.
    nhc.collect_devices()

    for device in nhc.devices:
        if isinstance(device, NHCManager.RelayDevice):
            if device.model == 'light':
                print(device)

    # Stop the application.
    nhc.stop()


if __name__ == '__main__':
    main()
