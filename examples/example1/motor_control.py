import time

import NHCManager

from config import *


def main():
    # Create a new NHC Manager.
    nhc = NHCManager.Manager()

    # Connect to the server
    nhc.connect(ADDRESS, PORT, USERNAME, PASSWORD, CERTIFICATE)

    # Start the connection (non-blocking).
    nhc.start()

    # Set a correct UUID for the motor action we want to control.
    # Not that we cannot control a motor directly, only an action that exists (such as a push button).
    motor_uuid = '15bfcc9a-30da-43ed-b9d2-839eaab50988'

    # Loop through all collected actions and compare the UUID, making sure it is in fact a motor action.
    motor = None
    for action in nhc.actions:
        if action.uuid == motor_uuid and isinstance(action, NHCManager.MotorAction):
            motor = action
            print(f'Found motor action \'{motor.name}\' with UUID {motor.uuid}')
            break

    if motor:
        position = 50
        print(f'Motor is currently at {motor.position}%')
        print(f'Setting position to {position}%')
        motor.position = position, False  # Non-blocking call to set the position

        print(f'Sleeping for approx. 3 seconds.')
        time.sleep(3)

        print(f'Stopping the motor now!')
        motor.stop()
        print(f'Motor is at {motor.position}%')
        motor.close()
    else:
        print(f'Motor action with UUID {motor_uuid} not found.')

    # Stop the application.
    nhc.stop()


if __name__ == '__main__':
    main()
