import typing

from .action import Action

if typing.TYPE_CHECKING:
    from ..manager import Manager


class TimeScheduleAction(Action):
    def __init__(self, manager: 'Manager', uuid: str, name: str, properties: typing.List[typing.Dict[str, str]]):
        super().__init__(manager, uuid, name)

        self._status: bool = False

        self.process_properties(properties)

    @property
    def status(self):
        return self._status

    def process_properties(self, properties: typing.List[typing.Dict[str, str]]):
        for property in properties:
            for key, value in property.items():
                match key:
                    case 'Active':
                        self._status = True if value.lower() == 'true' else False

                self._process_property_callback(key, value)
