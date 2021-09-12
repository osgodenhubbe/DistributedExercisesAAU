import random

from emulators.Device import Device
from emulators.Medium import Medium
from emulators.MessageStub import MessageStub


class GossipMessage(MessageStub):

    def __init__(self, sender: int, destination: int, secrets):
        super().__init__(sender, destination)
        # we use a set to keep the "secrets" here
        self.secrets = secrets

    def __str__(self):
        return f'{self.source} -> {self.destination} : {self.secrets}'


class Gossip(Device):

    def __init__(self, index: int, number_of_devices: int, medium: Medium):
        super().__init__(index, number_of_devices, medium)
        # for this exercise we use the index as the "secret", but it could have been a new routing-table (for instance)
        # or sharing of all the public keys in a cryptographic system
        self._secrets = set([index])

    def run(self):
        # the following is your termination condition, but where should it be placed?

        for device in range(0, self.number_of_devices()):
            if device == self.index():
                continue

            message = GossipMessage(self.index(), device, self._secrets)

            self.medium().send(message)

            ingoing = self.medium().receive()
            while ingoing is None:
                ingoing = self.medium().receive()

            self._secrets.add(ingoing.source)

            if len(self._secrets) == self._number_of_devices:
                return

        return

    def print_result(self):
        print(f'\tDevice {self.index()} got secrets: {self._secrets}')


class ImprovedGossip(Device):

    def __init__(self, index: int, number_of_devices: int, medium: Medium):
        super().__init__(index, number_of_devices, medium)
        # for this exercise we use the index as the "secret", but it could have been a new routing-table (for instance)
        # or sharing of all the public keys in a cryptographic system
        self._secrets = set([index])

    def run(self):
        # the following is your termination condition, but where should it be placed?

        if (self.index() == 0) and (len(self._secrets) <= 1):
            message = GossipMessage(self.index(), self.index()+1, self._secrets)
            self.medium().send(message)

        while True:
            print('Listening for message')
            ingoing = self.medium().receive()
            while ingoing is None:
                ingoing = self.medium().receive()
            print(f'Secrets before adding: {self._secrets}')
            self._secrets.update(ingoing.secrets)
            print(f'Secrets after adding: {self._secrets}')

            message = GossipMessage(self.index(), ((self.index()+1) % self._number_of_devices), self._secrets)
            self.medium().send(message)
            print('Message sent')

            if len(self._secrets) == self._number_of_devices:
                print('I have all secrets')
                return

        return

    def print_result(self):
        print(f'\tDevice {self.index()} got secrets: {self._secrets}')
