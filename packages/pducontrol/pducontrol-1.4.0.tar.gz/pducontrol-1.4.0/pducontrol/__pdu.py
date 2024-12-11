# This file is part of pdu-control
# Copyright (C) 2023 Safran
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
from typing import Union
from pducontrol.__pdu8100x import PDU8100X
from pducontrol.__pdu_swh_1023j import PDUControlREST


def choose_pdu(args: argparse.Namespace,
               credentials) -> Union[PDU8100X, PDUControlREST, None]:
    """Instantiate the correct class based on the PDU's IP

    Args:
        args: the previously parsed args
    Returns:
        If found, an instance of a supported PDU, else returns None
    """
    for pdu_class in [PDU8100X, PDUControlREST]:
        try:
            pdu = pdu_class(args.ip_address, **credentials)
            if pdu.get_outlet_status(1, .5):
                return pdu
        except Exception:
            pass

    return None
