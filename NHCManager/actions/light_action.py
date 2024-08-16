import typing

from .action import Action

if typing.TYPE_CHECKING:
    from ..manager import Manager


class LightAction(Action):
    def __init__(self, manager: 'Manager', uuid: str, name: str, properties: typing.List[typing.Dict[str, str]]):
        super().__init__(manager, uuid, name)

        self._status: bool = False

        self.process_properties(properties)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status: bool):
        _status = 'On' if status else 'Off'
        self.manager.device_control(self.uuid, {'Status': _status})

        # Wait for the device status changed event.
        while self.status != status:
            continue

    def process_properties(self, properties: typing.List[typing.Dict[str, str]]):
        for property in properties:
            for key, value in property.items():
                match key:
                    case 'Status':
                        self._status = True if value == 'On' else False
