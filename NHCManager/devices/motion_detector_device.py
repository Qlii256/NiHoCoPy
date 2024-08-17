import typing

from .device import Device

if typing.TYPE_CHECKING:
    from ..manager import Manager


class MotionDetectorDevice(Device):
    def __init__(self, manager: 'Manager', uuid: str, model: str, online: bool, name: str,
                 parameters: typing.List[typing.Dict[str, str]]):
        super().__init__(manager, uuid, model, online, name)

        self._location_id: str = ''
        self._motion_sensitivity: typing.Literal['Low', 'Medium', 'High', None] = None
        self._overrule_feedback_led: bool = False

        self.process_parameters(parameters)

    @property
    def location_id(self):
        return self._location_id

    @property
    def motion_sensitivity(self):
        return self._motion_sensitivity

    @property
    def overrule_feedback_led(self):
        return self._overrule_feedback_led

    def process_parameters(self, parameters: typing.List[typing.Dict[str, str]]):
        for parameter in parameters:
            for key, value in parameter.items():
                match key:
                    case 'LocationId':
                        self._location_id = value
                    case 'MotionSensitivity':
                        self._motion_sensitivity = value
                    case 'OverruleFeedbackLed':
                        self._overrule_feedback_led = True if value.lower() == 'enabled' else False

    def __repr__(self):
        return f'{super().__repr__()[:-1]} motion-sensitivity={self.motion_sensitivity}>'
