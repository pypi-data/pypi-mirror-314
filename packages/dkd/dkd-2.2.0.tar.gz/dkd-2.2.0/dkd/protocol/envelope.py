# -*- coding: utf-8 -*-
#
#   Dao-Ke-Dao: Universal Message Module
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2019 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

from abc import ABC, abstractmethod
from typing import Optional, Any, Dict

from mkm.types import DateTime
from mkm.types import Mapper
from mkm import ID


class Envelope(Mapper, ABC):
    """ This class is used to create a message envelope
        which contains 'sender', 'receiver' and 'time'

        Envelope for message
        ~~~~~~~~~~~~~~~~~~~~

        data format: {
            sender   : "moki@xxx",
            receiver : "hulk@yyy",
            time     : 123
        }
    """

    @property
    @abstractmethod
    def sender(self) -> ID:
        """
        Get message sender

        :return: sender ID
        """
        raise NotImplemented

    @property
    @abstractmethod
    def receiver(self) -> ID:
        """
        Get message receiver

        :return: receiver ID
        """
        raise NotImplemented

    @property
    @abstractmethod
    def time(self) -> Optional[DateTime]:
        """
        Get message time

        :return: timestamp
        """
        raise NotImplemented

    @property
    @abstractmethod
    def group(self) -> Optional[ID]:
        """
            Group ID
            ~~~~~~~~
            when a group message was split/trimmed to a single message
            the 'receiver' will be changed to a member ID, and
            the group ID will be saved as 'group'.
        """
        raise NotImplemented

    @group.setter
    @abstractmethod
    def group(self, value: ID):
        raise NotImplemented

    @property
    @abstractmethod
    def type(self) -> Optional[int]:
        """
            Message Type
            ~~~~~~~~~~~~
            because the message content will be encrypted, so
            the intermediate nodes(station) cannot recognize what kind of it.
            we pick out the content type and set it in envelope
            to let the station do its job.
        """
        raise NotImplemented

    @type.setter
    @abstractmethod
    def type(self, value: int):
        raise NotImplemented

    #
    #   Factory methods
    #

    @classmethod
    def create(cls, sender: ID, receiver: ID, time: DateTime = None):  # -> Envelope:
        gf = general_factory()
        return gf.create_envelope(sender=sender, receiver=receiver, time=time)

    @classmethod
    def parse(cls, envelope: Any):  # -> Optional[Envelope]:
        gf = general_factory()
        return gf.parse_envelope(envelope=envelope)

    @classmethod
    def factory(cls):  # -> EnvelopeFactory:
        gf = general_factory()
        return gf.get_envelope_factory()

    @classmethod
    def register(cls, factory):
        gf = general_factory()
        gf.set_envelope_factory(factory=factory)


def general_factory():
    from ..msg import MessageFactoryManager
    return MessageFactoryManager.general_factory


class EnvelopeFactory(ABC):

    @abstractmethod
    def create_envelope(self, sender: ID, receiver: ID, time: Optional[DateTime]) -> Envelope:
        """
        Create envelope

        :param sender:   sender ID
        :param receiver: receiver ID
        :param time:     message time
        :return: Envelope
        """
        raise NotImplemented

    @abstractmethod
    def parse_envelope(self, envelope: Dict[str, Any]) -> Optional[Envelope]:
        """
        Parse map object to envelope

        :param envelope: message head info
        :return: Envelope
        """
        raise NotImplemented
