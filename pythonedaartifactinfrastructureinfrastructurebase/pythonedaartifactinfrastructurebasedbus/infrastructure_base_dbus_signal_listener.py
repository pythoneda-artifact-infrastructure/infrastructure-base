"""
pythonedaartifactinfrastructureinfrastructurebase/pythonedaartifactinfrastructurebasedbus/infrastructure_base_dbus_signal_listener.py

This file defines the InfrastructureBaseDbusSignalListener class.

Copyright (C) 2023-today rydnr's pythoneda-artifact-infrastructure/infrastructure-base

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from pythoneda.event import Event
from pythonedaartifacteventgittagging.tag_credentials_provided import TagCredentialsProvided
from pythonedaartifacteventinfrastructuregittagging.pythonedaartifacteventgittaggingdbus.dbus_tag_created import DbusTagCreated
from pythonedainfrastructure.pythonedadbus.dbus_signal_listener import DbusSignalListener

from dbus_next import BusType, Message

from typing import Dict

class InfrastructureBaseDbusSignalListener(DbusSignalListener):

    """
    A Port that listens to InfrastructureBase-relevant d-bus signals.

    Class name: InfrastructureBaseDbusSignalListener

    Responsibilities:
        - Connect to d-bus.
        - Listen to signals relevant to InfrastructureBase.

    Collaborators:
        - PythonEDA: Receives relevant domain events.
    """

    def __init__(self):
        """
        Creates a new InfrastructureBaseDbusSignalListener instance.
        """
        super().__init__()

    def signal_receivers(self, app) -> Dict:
        """
        Retrieves the configured signal receivers.
        :param app: The PythonEDA instance.
        :type app: PythonEDA from pythonedaapplication.pythoneda
        :return: A dictionary with the signal name as key, and the tuple interface and bus type as the value.
        :rtype: Dict
        """
        result = {}
        key = self.fqdn_key(TagCreated)
        result[key] = [
            DbusTagCreatedentialsProvided, BusType.SYSTEM
        ]
        return result

    def parse_pythonedaartifactgittagging_TagCreated(self, message: Message) -> TagCreated:
        """
        Parses given d-bus message containing a TagCreated event.
        :param message: The message.
        :type message: dbus_next.Message
        :return: The TagCredentialsProvided event.
        :rtype: pythonedaartifacteventgittagging.tag_created.TagCreated
        """
        request_id, name, repository_url = message.body
        return TagCreated(request_id, name, repository_url)

    async def listen_pythonedaartifactgittagging_TagCreated(self, event: TagCreated):
        """
        Gets notified when a TagCreated event occurs.
        :param event: The TagCreated event.
        :type event: pythonedaartifactgittagging.tag_created.TagCreated
        """
        await self.app.accept(event)
