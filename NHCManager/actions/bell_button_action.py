import typing

from .action import Action

if typing.TYPE_CHECKING:
    from ..manager import Manager


class BellButtonAction(Action):
    def __init__(self, manager: 'Manager', uuid: str, name: str, parameters: typing.List[typing.Dict[str, str]],
                 properties: typing.List[typing.Dict[str, str]]):
        super().__init__(manager, uuid, name)

        self._status: bool = False
        self._triggered: bool = False
        self._door_lock: bool = False
        self._call_pending: bool = False
        self._call_answered: bool = False
        self._ringtone: typing.Literal['dunes', 'savanna', 'suburbia', 'rimbu', 'metropolis'] = 'dunes'
        self._decline_call_applied_on_all_devices: bool = False

        self.process_parameters(parameters)
        self.process_properties(properties)

    @property
    def status(self):
        return self._status

    @property
    def triggered(self):
        return self._triggered

    @property
    def door_lock(self):
        return self._door_lock

    @property
    def call_pending(self):
        return self._call_pending

    @property
    def call_answered(self):
        return self._call_answered

    @property
    def ringtone(self):
        return self._ringtone

    @property
    def decline_call_applied_on_all_devices(self):
        return self._decline_call_applied_on_all_devices

    def trigger(self):
        self.manager.device_control(self.uuid, {'BasicState': 'Triggered'})

        # Wait for the device status changed event.
        while not self.triggered:
            continue

    def trigger_door_lock(self):
        self.manager.device_control(self.uuid, {'Doorlock': 'Open'})

        # Wait for the device status changed event.
        while not self.door_lock:
            continue

    def process_parameters(self, parameters: typing.List[typing.Dict[str, str]]):
        for parameter in parameters:
            for key, value in parameter.items():
                match key:
                    case 'Ringtone':
                        self._ringtone = value.lower()
                    case 'DeclineCallAppliedOnAllDevices':
                        self._decline_call_applied_on_all_devices = True if value.lower() == 'true' else False

    def process_properties(self, properties: typing.List[typing.Dict[str, str]]):
        for property in properties:
            for key, value in property.items():
                match key:
                    case 'BasicState':
                        self._status = True if value.lower() == 'on' else False
                        self._triggered = True if value.lower() == 'triggered' else False
                    case 'Doorlock':
                        self._door_lock = True if value.lower() == 'open' else False
                    case 'CallPending':
                        self._call_pending = True if value.lower() == 'true' else False
                    case 'CallAnswered':
                        self._call_answered = True if value.lower() == 'true' else False

                self._process_property_callback(key, value)
