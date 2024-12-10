#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
nhcconnection.py

This is a tool to communicate with Niko Home Control.

You will have to provide an IP address and a port number.

License: MIT https://opensource.org/licenses/MIT
Source: https://github.com/NoUseFreak/niko-home-control
Author: Dries De Peuter
"""
import nclib
from .const import DEFAULT_PORT

NHC_TIMEOUT = 2000

class NHCConnection:
    """ A class to communicate with Niko Home Control. """
    def __init__(self, ip, port=DEFAULT_PORT):
        self._socket = None
        self._ip = ip
        self._port = port

    async def connect(self):
        """
        Connect to the Niko Home Control.
        """
        self._socket = nclib.Netcat((self._ip, self._port), udp=False)
        self._socket.settimeout(NHC_TIMEOUT)

    def __del__(self):
        self._socket.shutdown(1)
        self._socket.close()

    def receive(self):
        """
        Receives information from the Netcat socket.
        """
        return self._socket.recv().decode()

    def read(self):
        return self._receive_until(b'\r')

    def _receive_until(self, s):
        """
        Recieve data from the socket until the given substring is observed.
        Data in the same datagram as the substring, following the substring,
        will not be returned and will be cached for future receives.
        """
        return self._socket.recv_until(s)

    def send(self, s):
        """
        Sends the given command to Niko Home Control and returns the output of
        the system.

        Aliases: write, put, sendall, send_all
        """
        self._socket.send(s.encode())
        return self.read()
