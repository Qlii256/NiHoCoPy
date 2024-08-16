import typing

if typing.TYPE_CHECKING:
    from ..manager import Manager


class Action:
    def __init__(self, manager: 'Manager', uuid: str, name: str):
        self.manager = manager
        self.uuid: str = uuid
        self.name: str = name

    def process_properties(self, properties: typing.List[typing.Dict[str, str]]):
        raise NotImplementedError('Action.process_event should be implemented for all actions!')

    def __repr__(self):
        return (f'<{self.__class__.__name__} uuid={self.uuid} '
                f'name={self.name[:10] + "..." + self.name[-10:] if len(self.name) > 25 else self.name}>')
