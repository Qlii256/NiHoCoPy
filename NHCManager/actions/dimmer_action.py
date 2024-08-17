import typing

from .action import Action

if typing.TYPE_CHECKING:
    from ..manager import Manager


class DimmerAction(Action):
    def __init__(self, manager: 'Manager', uuid: str, name: str, properties: typing.List[typing.Dict[str, str]]):
        super().__init__(manager, uuid, name)

        self._status: bool = False
        self._brightness: int = 0

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

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, brightness: int):
        if isinstance(brightness, tuple):
            brightness, blocking = brightness
        else:
            blocking = True

        brightness = max(min(brightness, 100), 0)

        if brightness == self.brightness:
            return

        self.manager.device_control(self.uuid,
                                    {
                                        'Status': 'On',
                                        'Brightness': str(brightness)
                                    })

        if blocking:
            # Wait for the device status changed event.
            while self.brightness != brightness:
                continue
        else:
            # Force the changed value.
            # This can lead to the value being desynchronized when an error is returned by the controller.
            self._brightness = brightness

    def process_properties(self, properties: typing.List[typing.Dict[str, str]]):
        for property in properties:
            for key, value in property.items():
                match key:
                    case 'Status':
                        self._status = True if value.lower() == 'on' else False
                    case 'Brightness':
                        self._brightness = int(value)

                self._process_property_callback(key, value)
