import typing

from .connection import Connection
from .devices import *
from .actions import *


class Manager:
    def __init__(self):
        self.connection = Connection()

        self._message_queue = {'devices.list': [], 'devices.status': []}

        self.devices = []
        self.actions = []

        # Set callback for received messages
        self.connection.on_message = self._on_message

    def connect(self, address: str, port: int, username: str, password: str, certificate: str):
        self.connection.connect(address, port, username, password, certificate)

    def start(self):
        self.connection.start()

        self.collect_devices()

    def stop(self):
        self.connection.stop()

    def collect_devices(self):
        """This method collects all available devices in the NHC project. It stores their status, parameters, properties
         and more. This method is run automatically at Manager.start and should not be called by the user."""
        self.connection.publish('hobby/control/devices/cmd', {'Method': 'devices.list'})

        while not len(self._message_queue['devices.list']):
            continue
        devices = self._message_queue['devices.list'].pop()['Params'][0]['Devices']

        actions = []
        _devices = []
        for device in devices:
            if device['Type'] == 'action':
                action = None
                match device['Model']:
                    case 'rolldownshutter' | 'sunblind' | 'gate' | 'venetianblind':
                        action = MotorAction(
                            manager=self,
                            uuid=device['Uuid'],
                            name=device['Name'],
                            properties=device['Properties'])
                    case 'dimmer':
                        action = DimmerAction(
                            manager=self,
                            uuid=device['Uuid'],
                            name=device['Name'],
                            properties=device['Properties'])
                    # case _:
                    #     continue
                    #     print(f'Device type \'{device["Model"]}\' cannot be recognized.')

                if action:
                    actions.append(action)
            else:
                _device = None
                match device['Type']:
                    case 'motor':
                        _device = MotorDevice(
                            manager=self,
                            uuid=device['Uuid'],
                            model=device['Model'],
                            online=device['Online'],
                            name=device['Name'],
                            parameters=device['Parameters'],
                            traits=device['Traits'])
                    case 'panel':
                        _device = PanelDevice(
                            manager=self,
                            uuid=device['Uuid'],
                            model=device['Model'],
                            online=device['Online'],
                            name=device['Name'],
                            parameters=device['Parameters'])
                    case 'virtual':
                        _device = VirtualDevice(
                            manager=self,
                            uuid=device['Uuid'],
                            model=device['Model'],
                            online=device['Online'],
                            name=device['Name'],
                            parameters=device['Parameters'],
                            properties=device['Properties'])
                    case 'digitalsensor':
                        _device = DigitalSensorDevice(
                            manager=self,
                            uuid=device['Uuid'],
                            model=device['Model'],
                            online=device['Online'],
                            name=device['Name'],
                            parameters=device['Parameters'],
                            traits=device['Traits'])
                    case 'motiondetector':
                        _device = MotionDetectorDevice(
                            manager=self,
                            uuid=device['Uuid'],
                            model=device['Model'],
                            online=device['Online'],
                            name=device['Name'],
                            parameters=device['Parameters'])
                    case 'relay':
                        _device = RelayDevice(
                            manager=self,
                            uuid=device['Uuid'],
                            model=device['Model'],
                            online=device['Online'],
                            name=device['Name'],
                            parameters=device['Parameters'],
                            traits=device['Traits'])
                if _device:
                    _devices.append(_device)

        self.actions = actions
        self.devices = _devices

    def device_control(self, uuid: str, properties: typing.Dict[str, str]):
        self.connection.publish('hobby/control/devices/cmd', {'Method': 'devices.control',
                                                              'Params': [
                                                                  {
                                                                      'Devices': [
                                                                          {
                                                                              'Properties': [properties],
                                                                              'Uuid': uuid
                                                                          }
                                                                      ]
                                                                  }
                                                              ]})

    def _process_event(self, data):
        if data['Method'] == 'devices.status':
            uuid = data['Params'][0]['Devices'][0]['Uuid']

            online = data['Params'][0]['Devices'][0].get('Online')
            properties = data['Params'][0]['Devices'][0].get('Properties')

            # If properties are given, it's possible we are dealing with an action.
            if properties:
                for action in self.actions:
                    if action.uuid == uuid:
                        action.process_properties(properties)
                        return

            for device in self.devices:
                if device.uuid == uuid:
                    if online:
                        device.online = True if online == 'True' else False
                        print(f'Set online to {device.online} for {device.name}')
                    device.process_properties(properties)
                    break
            # else:
            #     raise ValueError(data)

    def on_message(self, topic: str, data: dict):
        pass

    def _on_message(self, topic: str, data: dict):
        match topic:
            case 'hobby/control/devices/rsp':
                if data['Method'] == 'devices.list':
                    self._message_queue['devices.list'].append(data)
                elif data['Method'] == 'devices.status':
                    self._message_queue['devices.status'].append(data)
            case 'hobby/control/devices/evt':
                self._process_event(data)
            case 'hobby/control/devices/err':
                raise Exception(data)
            case _:
                self.on_message(topic, data)
