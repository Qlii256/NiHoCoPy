import typing

from .action import Action

if typing.TYPE_CHECKING:
    from ..manager import Manager


class GenericAction(Action):
    def __init__(self, manager: 'Manager', uuid: str, name: str, properties: typing.List[typing.Dict[str, str]]):
        super().__init__(manager, uuid, name)

        self._status: bool = False
        self._triggered: bool = False
        self._start_text: str = ''
        self._stop_text: str = ''
        self._start_active: bool = False
        self._all_started: bool = False

        self.process_properties(properties)

    @property
    def status(self):
        return self._status

    @property
    def triggered(self):
        return self._triggered

    @property
    def start_text(self):
        return self._start_text

    @property
    def stop_text(self):
        return self._stop_text

    @property
    def start_active(self):
        return self._start_active

    @property
    def all_started(self):
        return self._all_started

    def trigger(self):
        self.manager.device_control(self.uuid, {'BasicState': 'Triggered'})

        # Wait for the device status changed event.
        while not self.triggered:
            continue

    def process_properties(self, properties: typing.List[typing.Dict[str, str]]):
        for property in properties:
            for key, value in property.items():
                match key:
                    case 'BasicState':
                        self._status = True if value.lower() == 'on' else False
                        self._triggered = True if value.lower() == 'triggered' else False
                    case 'StartText':
                        self._start_text = value
                    case 'StopText':
                        self._stop_text = value
                    case 'StartActive':
                        self._start_active = True if value.lower() == 'true' else False
                    case 'AllStarted':
                        self._all_started = True if value.lower() == 'true' else False

                self._process_property_callback(key, value)
