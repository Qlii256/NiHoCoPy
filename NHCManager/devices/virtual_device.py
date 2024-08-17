import typing

from .device import Device

if typing.TYPE_CHECKING:
    from ..manager import Manager


class VirtualDevice(Device):
    def __init__(self, manager: 'Manager', uuid: str, model: str, online: bool, name: str,
                 parameters: typing.List[typing.Dict[str, str]], properties: typing.List[typing.Dict[str, str]]):
        super().__init__(manager, uuid, model, online, name)

        self._location_id: str = ''
        self._status: bool = False

        self.process_parameters(parameters)
        self.process_properties(properties)

    @property
    def location_id(self):
        return self._location_id

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status: bool):
        _status = 'True' if status else 'False'
        self.manager.device_control(self.uuid, {'Status': _status})

        # Wait for the device status changed event.
        while self.status != status:
            continue

    def process_parameters(self, parameters: typing.List[typing.Dict[str, str]]):
        for parameter in parameters:
            for key, value in parameter.items():
                match key:
                    case 'LocationId':
                        self._location_id = value

    def process_properties(self, properties: typing.List[typing.Dict[str, str]]):
        for property in properties:
            for key, value in property.items():
                match key:
                    case 'Status':
                        self._status = True if value.lower() == 'true' else False

    def __repr__(self):
        return f'{super().__repr__()[:-1]} status={self.status}>'
