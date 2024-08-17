import typing

if typing.TYPE_CHECKING:
    from ..manager import Manager


class Device:
    def __init__(self, manager: 'Manager', uuid: str, model: str, online: bool, name: str):
        self.manager = manager
        self.uuid = uuid
        self.model = model
        self.online = online
        self.name = name

    def __repr__(self):
        return (f'<{self.__class__.__name__} uuid={self.uuid} '
                f'name={self.name[:10] + "..." + self.name[-10:] if len(self.name) > 25 else self.name}>')
