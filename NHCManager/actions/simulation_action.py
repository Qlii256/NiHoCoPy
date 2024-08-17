import typing

from .action import Action

if typing.TYPE_CHECKING:
    from ..manager import Manager


class SimulationAction(Action):
    def __init__(self, manager: 'Manager', uuid: str, name: str, properties: typing.List[typing.Dict[str, str]]):
        super().__init__(manager, uuid, name)

        self._status: bool = False
        self._triggered: bool = False

        self.process_properties(properties)

    @property
    def status(self):
        return self._status

    @property
    def triggered(self):
        return self._triggered

    def trigger(self):
        self.manager.device_control(self.uuid, {'BasicState': 'Triggered'})

        # Wait for the device status changed event.
        while self.triggered:
            continue

    def process_properties(self, properties: typing.List[typing.Dict[str, str]]):
        for property in properties:
            for key, value in property.items():
                match key:
                    case 'BasicState':
                        self._status = True if value.lower() == 'on' else False
                        self._triggered = True if value.lower() == 'triggered' else False

                self._process_property_callback(key, value)
