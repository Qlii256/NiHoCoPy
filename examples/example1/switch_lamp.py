import NHCManager

from config import *


def main():
    # Create a new NHC Manager.
    nhc = NHCManager.Manager()

    # Connect to the server
    nhc.connect(ADDRESS, PORT, USERNAME, PASSWORD, CERTIFICATE)

    # Start the connection (non-blocking).
    nhc.start()

    # Set a correct name for the lamp action we want to control.
    # Not that we cannot control a lamp directly, only an action that exists (such as a basic action).
    lamp_name = 'My Lamp Basic Action'

    # Loop through all collected actions and compare the name, making sure it is in fact a light action.
    for action in nhc.actions:
        if action.name == lamp_name and isinstance(action, NHCManager.LightAction):
            action.status = True  # Switch the lamp on.

    # Stop the application.
    nhc.stop()


if __name__ == '__main__':
    main()
