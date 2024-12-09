#
#  --------------------------------------------------------------------------
#   Gurux Ltd
#
#
#
#  Filename: $HeadURL$
#
#  Version: $Revision$,
#                   $Date$
#                   $Author$
#
#  Copyright (c) Gurux Ltd
#
# ---------------------------------------------------------------------------
#
#   DESCRIPTION
#
#  This file is a part of Gurux Device Framework.
#
#  Gurux Device Framework is Open Source software; you can redistribute it
#  and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; version 2 of the License.
#  Gurux Device Framework is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  More information of Gurux products: http://www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http://www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
from gurux_dlms.enums import InterfaceType, Authentication, Security, Standard
from gurux_dlms import GXDLMSClient
from gurux_dlms.GXByteBuffer import GXByteBuffer
from gurux_dlms.objects import GXDLMSObject
from gurux_common.enums import TraceLevel
from gurux_common.io import Parity, StopBits, BaudRate
from gurux_net.enums import NetworkType
from gurux_net import GXNet
from gurux_serial.GXSerial import GXSerial
from .GXDLMSSecureClient2 import GXDLMSSecureClient2

class GXSettings:
    #
    # Constructor.
    #
    def __init__(self):
        self.media = None
        self.trace = TraceLevel.INFO
        self.invocationCounter = None
        self.client = GXDLMSSecureClient2(True)
        #  Objects to read.
        self.readObjects = []
        self.outputFile = None
