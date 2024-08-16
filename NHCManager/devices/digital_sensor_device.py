import typing

from .device import Device

if typing.TYPE_CHECKING:
    from ..manager import Manager


class DigitalSensorDevice(Device):
    def __init__(self, manager: 'Manager', uuid: str, model: str, online: bool, name: str,
                 parameters: typing.List[typing.Dict[str, str]], traits: typing.List[typing.Dict[str, str]]):
        super().__init__(manager, uuid, model, online, name)

        self._location_id: str = ''
        self._inverted: bool = False
        self._channel: int = 0

        self.process_parameters(parameters)
        self.process_traits(traits)

    @property
    def location_id(self):
        return self._location_id

    @property
    def inverted(self):
        return self._inverted

    @property
    def channel(self):
        return self._channel

    def process_parameters(self, parameters: typing.List[typing.Dict[str, str]]):
        for parameter in parameters:
            for key, value in parameter.items():
                match key:
                    case 'LocationId':
                        self._location_id = value
                    case 'Inverted':
                        self._inverted = True if value == 'True' else False

    def process_traits(self, traits: typing.List[typing.Dict[str, str]]):
        for trait in traits:
            for key, value in trait.items():
                match key:
                    case 'Channel':
                        self._channel = int(value)

    def __repr__(self):
        return f'{super().__repr__()[:-1]} inverted={self.inverted} channel={self.channel}>'
