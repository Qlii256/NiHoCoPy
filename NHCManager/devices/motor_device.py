import typing

from .device import Device

if typing.TYPE_CHECKING:
    from ..manager import Manager


class MotorDevice(Device):
    def __init__(self, manager: 'Manager', uuid: str, model: str, online: bool, name: str,
                 parameters: typing.List[typing.Dict[str, str]], traits: typing.List[typing.Dict[str, str]]):
        super().__init__(manager, uuid, model, online, name)

        self._location_id: str = ''
        self._stepping_pulse: float = 0
        self._venetian_blind_type: typing.Literal[
            'rolldownshutter', 'sunblind', 'gate', 'venetianblind'] = 'venetianblind'
        self._open_run_time: int = 0
        self._close_run_time: int = 0

        self._channel: int = 0

        self.process_parameters(parameters)
        self.process_traits(traits)

    @property
    def location_id(self):
        return self._location_id

    @property
    def stepping_pulse(self):
        return self._stepping_pulse

    @property
    def venetian_blind_type(self):
        return self._venetian_blind_type

    @property
    def open_run_time(self):
        return self._open_run_time

    @property
    def close_run_time(self):
        return self._close_run_time

    @property
    def channel(self):
        return self._channel

    def process_parameters(self, parameters: typing.List[typing.Dict[str, str]]):
        for parameter in parameters:
            for key, value in parameter.items():
                match key:
                    case 'LocationId':
                        self._location_id = value
                    case 'SteppingPulse':
                        self._stepping_pulse = float(value)
                    case 'VenetianBlindType':
                        self._venetian_blind_type = value
                    case 'OpenRunTime':
                        self._open_run_time = int(value)
                    case 'CloseRunTime':
                        self._close_run_time = int(value)

    def process_traits(self, traits: typing.List[typing.Dict[str, str]]):
        for trait in traits:
            for key, value in trait.items():
                match key:
                    case 'Channel':
                        self._channel = int(value)

    def __repr__(self):
        return f'{super().__repr__()[:-1]} stepping-pulse={self.stepping_pulse}>'
