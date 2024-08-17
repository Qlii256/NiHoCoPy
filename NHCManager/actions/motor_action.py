import typing

from .action import Action

if typing.TYPE_CHECKING:
    from ..manager import Manager


class MotorAction(Action):
    def __init__(self, manager: 'Manager', uuid: str, name: str, properties: typing.List[typing.Dict[str, str]]):
        super().__init__(manager, uuid, name)

        self._last_direction: typing.Literal['Open', 'Close'] = 'Open'
        self._position: int = 0
        self._moving: bool = False

        self.process_properties(properties)

    @property
    def last_direction(self):
        return self._last_direction

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position: int):
        if isinstance(position, tuple):
            position, blocking = position
        else:
            blocking = True

        position = max(min(position, 100), 0)

        if position == self.position:
            return

        self.manager.device_control(self.uuid, {'Position': str(position)})

        # Force moving to True
        self._moving = True

        if blocking:
            # Wait for the device status changed event.
            while self.moving:
                continue
        else:
            # Force the changed value.
            # This can lead to the value being desynchronized when an error is returned by the controller.
            self._position = position

    @property
    def moving(self):
        return self._moving

    def open(self, blocking: bool = True):
        self.manager.device_control(self.uuid, {'Action': 'Open'})

        # Force moving to True
        self._moving = True

        if blocking:
            # Wait for the device status changed event.
            while self.moving:
                continue
        else:
            # Force the changed value.
            # This can lead to the value being desynchronized when an error is returned by the controller.
            self._moving = False

    def close(self, blocking: bool = True):
        self.manager.device_control(self.uuid, {'Action': 'Close'})

        # Force moving to True
        self._moving = True

        if blocking:
            # Wait for the device status changed event.
            while self.moving:
                continue
        else:
            # Force the changed value.
            # This can lead to the value being desynchronized when an error is returned by the controller.
            self._moving = False

    def stop(self, blocking: bool = True):
        self.manager.device_control(self.uuid, {'Action': 'Stop'})

        if blocking:
            # Wait for the device status changed event.
            while self.moving:
                continue
        else:
            # Force the changed value.
            # This can lead to the value being desynchronized when an error is returned by the controller.
            self._moving = False

    def process_properties(self, properties: typing.List[typing.Dict[str, str]]):
        for property in properties:
            for key, value in property.items():
                match key:
                    case 'LastDirection':
                        self._last_direction = value
                    case 'Position':
                        self._position = int(value)
                    case 'Moving':
                        self._moving = True if value.lower() == 'true' else False

                self._process_property_callback(key, value)
