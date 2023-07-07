"""
pythonedaartifactinfrastructureinfrastructurebase/pythonedaartifactinfrastructurebasedbus/infrastructure_base_dbus_signal_emitter.py

This file defines the InfrastructureBaseDbusSignalEmitter class.

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
from pythonedaartifacteventgittagging.tag_created import TagCreated
from pythonedaartifacteventgittagging.tag_requested import TagRequested
from pythonedaartifacteventinfrastructuregittagging.pythonedaartifacteventinfrastructurebasedbus.dbus_tag_created import DbusTagCreated
from pythonedaartifacteventinfrastructuregittagging.pythonedaartifacteventinfrastructurebasedbus.dbus_tag_requested import DbusTagRequested
from pythonedainfrastructure.pythonedadbus.dbus_signal_emitter import DbusSignalEmitter

import asyncio
from dbus_next.aio import MessageBus
from dbus_next import BusType, Message, MessageType

from typing import Dict, List

class InfrastructureBaseDbusSignalEmitter(DbusSignalEmitter):

    """
    A Port that emits GitTagging events as d-bus signals.

    Class name: InfrastructureBaseDbusSignalEmitter

    Responsibilities:
        - Connect to d-bus.
        - Emit domain events as d-bus signals on behalf of InfrastructureBase.

    Collaborators:
        - PythonEDA: Requests emitting events.
    """
    def __init__(self):
        """
        Creates a new InfrastructureBaseDbusSignalEmitter instance.
        """
        super().__init__()

    def transform_TagRequested(self, event: TagRequested) -> List[str]:
        """
        Transforms given event to signal parameters.
        :param event: The event to transform.
        :type event: pythonedaartifacteventgittagging.tag_requested.TagRequested
        :return: The event information.
        :rtype: List[str]
        """
        return [ event.repository_url, event.branch ]

    def signature_for_TagRequested(self, event: TagRequested) -> str:
        """
        Retrieves the signature for the parameters of given event.
        :param event: The domain event.
        :type event: pythonedaartifacteventgittagging.tag_requested.TagRequested
        :return: The signature.
        :rtype: str
        """
        return 'ss'

    def transform_TagCreated(self, event: TagCreated) -> List[str]:
        """
        Transforms given event to signal parameters.
        :param event: The event to transform.
        :type event: pythonedaartifacteventgittagging.tag_created.TagCreated
        :return: The event information.
        :rtype: List[str]
        """
        return [ event.name, event.repository_url ]

    def signature_for_TagCreated(self, event: TagCreated) -> str:
        """
        Retrieves the signature for the parameters of given event.
        :param event: The domain event.
        :type event: pythonedaartifacteventgittagging.tag_created.TagCreated
        :return: The signature.
        :rtype: str
        """
        return 'ss'

    def emitters(self) -> Dict:
        """
        Retrieves the configured event emitters.
        :return: A dictionary with the event class name as key, and a dictionary as value. Such dictionary must include the following entries:
          - "interface": the event interface,
          - "busType": the bus type,
          - "transformer": a function capable of transforming the event into a string.
          - "signature": a function capable of returning the types of the event parameters.
        :rtype: Dict
        """
        result = {}
        tag_requested_key, tag_requested_config = self.emitter_for_TagRequested()
        result[tag_requested_key] = tag_requested_config
        return result

    def emitter_for_TagRequested(self) -> Dict:
        """
        Retrieves the event emitter configuration for TagRequested.
        :return: A tuple: the event class name, and a that dictionary must include the following entries:
          - "interface": the event interface,
          - "busType": the bus type,
          - "transformer": a function capable of transforming the event into a string.
          - "signature": a function capable of returning the types of the event parameters.
        :rtype: tuple
        """
        key = self.fqdn_key(TagRequested)
        return key, {
                "interface": DbusTagRequested,
                "busType": BusType.SYSTEM,
                "transformer": self.transform_TagRequested,
                "signature": self.signature_for_TagRequested
            }

