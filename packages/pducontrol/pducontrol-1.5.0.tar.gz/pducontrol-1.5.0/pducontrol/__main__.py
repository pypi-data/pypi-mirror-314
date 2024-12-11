# This file is part of pdu-control
# Copyright (C) 2024 Safran
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

import sys
import argcomplete

from .__cli import get_credentials, get_parser, name_to_address
from .__pdu import choose_pdu


def main() -> None:
    """Called when using CLI"""
    parser = get_parser()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    args.ip_address = name_to_address(args.ip_address)
    pdu = choose_pdu(args, get_credentials(args))

    if pdu is None:
        print("No supported device found or invalid credentials, please check "
              "your information.")
        sys.exit(1)

    args.func(args, pdu)


if __name__ == "__main__":
    main()
