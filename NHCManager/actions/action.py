import threading
import typing

if typing.TYPE_CHECKING:
    from ..manager import Manager


class Action:
    def __init__(self, manager: 'Manager', uuid: str, name: str):
        self.manager = manager
        self.uuid: str = uuid
        self.name: str = name

        self._callbacks: typing.Dict[str, typing.List[typing.Callable]] = {}

    def set_property_callback(self, property: str, callback: typing.Callable):
        if property not in self._callbacks:
            self._callbacks[property] = []

        self._callbacks[property].append(callback)

    def _process_property_callback(self, property: str, value: typing.Union[int, str]):
        # Execute callbacks each in their own thread as to not block the current thread.
        if property in self._callbacks:
            for callback in self._callbacks[property]:
                threading.Thread(target=callback, args=(value,), daemon=True).start()

    def __repr__(self):
        return (f'<{self.__class__.__name__} uuid={self.uuid} '
                f'name={self.name[:10] + "..." + self.name[-10:] if len(self.name) > 25 else self.name}>')
