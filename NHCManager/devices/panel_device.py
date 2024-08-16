import typing

from .device import Device

if typing.TYPE_CHECKING:
    from ..manager import Manager


class PanelDeviceButton:
    def __init__(self):
        self._long_press_time: int = 0
        self._button_mode: typing.Literal['ShortPress', 'LongPress', 'PressRelease'] = 'ShortPress'

    @property
    def long_press_time(self):
        return self._long_press_time

    @property
    def button_mode(self):
        return self._button_mode

    def __repr__(self):
        return (f'<{self.__class__.__name__} long-press-time={self.long_press_time} '
                f'button-mode={self.button_mode}>')


class PanelDevice(Device):
    def __init__(self, manager: 'Manager', uuid: str, model: str, online: bool, name: str,
                 parameters: typing.List[typing.Dict[str, str]]):
        super().__init__(manager, uuid, model, online, name)

        self._location_id: str = ''

        self.buttons: typing.List[PanelDeviceButton] = []

        match model:
            case 'motorcontroller':
                num_of_buttons = 4
            case 'dimcontroller':
                num_of_buttons = 0
            case _:
                num_of_buttons = int(model.replace('feedback', '')[-1:])

        for i in range(num_of_buttons):
            self.buttons.append(PanelDeviceButton())

        self.process_parameters(parameters)

    @property
    def location_id(self):
        return self._location_id

    def process_parameters(self, parameters: typing.List[typing.Dict[str, str]]):
        for parameter in parameters:
            for key, value in parameter.items():
                match key:
                    case 'LocationId':
                        self._location_id = value
                    case s if s.startswith('LongPressTime'):
                        self.buttons[int(s[-1:]) - 1]._long_press_time = int(value.rsplit('.')[0])
                    case s if s.startswith('ButtonMode'):
                        self.buttons[int(s[-1:]) - 1]._button_mode = value
