import random
import time

import NHCManager

from config import *


def random_brightness(dimmable_lamp: NHCManager.DimmerAction):
    # The brightness value we should dim the lamp to.
    brightness = random.randint(0, 100)

    print(f'Brightness is currently at {dimmable_lamp.brightness}%')
    print(f'Setting brightness to {brightness}%')
    dimmable_lamp.brightness = brightness
    print(f'Brightness is at {dimmable_lamp.brightness}%')


def wave_effect(dimmable_lamp: NHCManager.DimmerAction):
    dimming_time = 2

    # Set the brightness to 0 to start and wait for 1 sec.
    dimmable_lamp.brightness = 0
    time.sleep(1)

    # Increase the brightness by 50% and wait half the dimming time, then increase another 50%.
    # After waiting another half of the dimming time, we decrease the same steps towards 0%.
    # Note that this is not working exactly as the Dimming time available in the NHC Programming software, as that value
    # is not available through the Hobby API.
    while True:
        dimmable_lamp.brightness = dimmable_lamp.brightness + 50, False
        time.sleep(dimming_time * .5)
        dimmable_lamp.brightness = dimmable_lamp.brightness + 50, False
        time.sleep(dimming_time * .5)

        dimmable_lamp.brightness = dimmable_lamp.brightness - 50, False
        time.sleep(dimming_time * .5)
        dimmable_lamp.brightness = dimmable_lamp.brightness - 50, False
        time.sleep(dimming_time * .5)


def main():
    # Create a new NHC Manager.
    nhc = NHCManager.Manager()

    # Connect to the server
    nhc.connect(ADDRESS, PORT, USERNAME, PASSWORD, CERTIFICATE)

    # Start the connection (non-blocking).
    nhc.start()

    # Set a correct UUID for the dimmable lamp action we want to control.
    # Not that we cannot control a dimmable lamp directly, only an action that exists (such as a push button).
    dimmable_lamp_uuid = '26e80fc2-1278-4a2d-b2c2-22d9b04c68b6'

    # Loop through all collected actions and compare the UUID, making sure it is in fact a dimmer action.
    dimmable_lamp = None
    for action in nhc.actions:
        if action.uuid == dimmable_lamp_uuid and isinstance(action, NHCManager.DimmerAction):
            dimmable_lamp = action
            print(f'Found dimmable lamp action \'{dimmable_lamp.name}\' with UUID {dimmable_lamp.uuid}')
            break

    if dimmable_lamp:
        # Set the brightness and turn the lamp off.
        dimmable_lamp.brightness = 30
        dimmable_lamp.status = False

        # Set a random brightness and turn the lamp on.
        # random_brightness(dimmable_lamp)

        # Create a wave-like effect by having the lamp go on and off in a loop.
        # wave_effect(dimmable_lamp)
    else:
        print(f'Dimmable lamp action with UUID {dimmable_lamp_uuid} not found.')

    # Stop the application.
    nhc.stop()


if __name__ == '__main__':
    main()
