import time

import NHCManager

from config import *


# USAGE
#
# Create a basic action (SwitchedGenericAction) in the NHC Programming software between a (push)button and a virtual
# flag. Name the action and use its name in the `cancel_call_action_name` variable. Make sure the button is set to
# `push-button mode` (PressRelease). Paste the name of the panel on which the button resides into the
# `cancel_call_panel_name` variable.
#
# Locate the routine for the intercom system (bell) and paste its name into the `bell_routine_name` variable.
# Run the script and ring the bell. Before the ring time-out, press the configured cancel button and the pending call
# should stop (on all devices if configured correctly).

def main():
    # Create a new NHC Manager.
    nhc = NHCManager.Manager()

    # Connect to the server
    nhc.connect(ADDRESS, PORT, USERNAME, PASSWORD, CERTIFICATE)

    # Start the connection (non-blocking).
    nhc.start()

    # Configuration
    cancel_call_panel_name = 'Tweevoudige drukknop Woonkamer - Bureel (Ruben)'
    cancel_call_action_name = 'Stop inkomende oproep (Bel voordeur)'
    bell_routine_name = 'Bel voordeur'
    cancel_call_panel_button_index = 0  # The index of the button on the panel that will be pressed.

    # These values will be set automatically.
    bell_routine = None  # The bell routine (intercom).
    cancel_call_action = None  # The SwitchedGenericAction (basic action) that will be checked if active.
    cancel_call_panel = None  # The PanelDevice on which the button resides.

    # Try to find the correct actions.
    for action in nhc.actions:
        if action.name == bell_routine_name and isinstance(action, NHCManager.BellButtonAction):
            bell_routine = action
        if action.name == cancel_call_action_name and isinstance(action, NHCManager.SwitchedGenericAction):
            cancel_call_action = action

    # Find the correct panel.
    for device in nhc.devices:
        if device.name == cancel_call_panel_name and isinstance(device, NHCManager.PanelDevice):
            if device.buttons[cancel_call_panel_button_index].button_mode == 'PressRelease':
                cancel_call_panel = device

    if not bell_routine or not cancel_call_action or not cancel_call_panel:
        raise ValueError('Missing one of the 3 required components!')

    def cancel_call_action_triggered(value):
        # We get the raw value back straight from the API here using the callback.
        # This way we do not need to check every x amount of time in a loop, but can just do something else while we
        # wait for the callback on the property 'Status' for the SwitchedGenericAction.
        if value.lower() == 'on':
            print('Cancel call triggered')
            if bell_routine.call_pending:
                print('Call is pending...')
                bell_routine.trigger()
                print('Call is stopped')

    # Set a callback on the 'Status' property for the basic action that is switched when the button is pressed.
    cancel_call_action.set_property_callback('Status', cancel_call_action_triggered)

    try:
        # Keep the application running.
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        pass

    # Stop the application.
    nhc.stop()


if __name__ == '__main__':
    main()
