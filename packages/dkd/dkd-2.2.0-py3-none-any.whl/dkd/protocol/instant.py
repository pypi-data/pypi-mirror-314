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

from .content import Content
from .envelope import Envelope
from .message import Message


class InstantMessage(Message, ABC):
    """
        Instant Message
        ~~~~~~~~~~~~~~~

        data format: {
            //-- envelope
            sender   : "moki@xxx",
            receiver : "hulk@yyy",
            time     : 123,
            //-- content
            content  : {...}
        }
    """

    @property
    @abstractmethod
    def content(self) -> Content:
        """ message content """
        raise NotImplemented

    # @content.setter
    # def content(self, value: Content):
    #     """ only for rebuild content """
    #     raise NotImplemented

    #
    #   Factory methods
    #

    @classmethod
    def create(cls, head: Envelope, body: Content):  # -> InstantMessage:
        gf = general_factory()
        return gf.create_instant_message(head=head, body=body)

    @classmethod
    def parse(cls, msg: Any):  # -> Optional[InstantMessage]:
        gf = general_factory()
        return gf.parse_instant_factory(msg=msg)

    @classmethod
    def generate_serial_number(cls, msg_type: int, now: DateTime) -> int:
        gf = general_factory()
        return gf.generate_serial_number(msg_type, now)

    @classmethod
    def factory(cls):  # -> Optional[InstantMessageFactory]:
        gf = general_factory()
        return gf.get_instant_message_factory()

    @classmethod
    def register(cls, factory):
        gf = general_factory()
        gf.set_instant_message_factory(factory=factory)


def general_factory():
    from ..msg import MessageFactoryManager
    return MessageFactoryManager.general_factory


class InstantMessageFactory(ABC):

    @abstractmethod
    def generate_serial_number(self, msg_type: int, now: DateTime) -> int:
        """
        Generate SN for message content

        :param msg_type: content type
        :param now:      message time
        :return: SN (uint64, serial number as msg id)
        """
        raise NotImplemented

    @abstractmethod
    def create_instant_message(self, head: Envelope, body: Content) -> InstantMessage:
        """
        Create instant message with envelope & content

        :param head: message envelope
        :param body: message content
        :return: InstantMessage
        """
        raise NotImplemented

    @abstractmethod
    def parse_instant_message(self, msg: Dict[str, Any]) -> Optional[InstantMessage]:
        """
        Parse map object to message

        :param msg: message info
        :return: InstantMessage
        """
        raise NotImplemented
