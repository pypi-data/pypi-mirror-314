#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

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

from typing import List, Optional

import requests
import xmltodict


class PDUControlREST:
    """Class used to control the SWH 1023J PDU from the LU test farm"""

    def __init__(self, ip: str, user: str = "snmp", password: str = "1234"):
        self.ip = f"http://{user}:{password}@{ip}/"

    available_cmd = {
        "on": 1,
        "off": 0,
        "reboot": 2,
    }
    available_cmd_reverse = {
        0: "off",
        1: "on",
        2: "reboot",
    }

    @staticmethod
    def get_total_outlets() -> int:
        """
        This method exists to keep the same code structure as the one
        used to control the ROC PDU
        """
        return 8

    def get_all_outlet_statuses(self, timeout=None) -> Optional[List[str]]:
        """
        Returns the state of all the outlets
        Returns:
            list[str]: List containing the state of all outlets
        """
        r = requests.get(
            self.ip + "status.xml",
            timeout=timeout
        )
        if r.status_code != 200:
            return None
        else:
            data = xmltodict.parse(r.text)
            status = data["response"]["pot0"][2:].split(",")[8:16]
            return [self.available_cmd_reverse[int(s)] for s in status]

    def get_outlet_status(self, outlet: int = 1, timeout=None
                          ) -> Optional[str]:
        """
        Returns the state of a specific outlet
        Args:
            outlet: ID of the outlet (from 1 to 8)
            timeout: max time without answer

        Returns
            str: State of the desired outlet
        """
        if type(outlet) != int or outlet <= 0:
            raise ValueError("outlet must be a positive integer")
        return self.get_all_outlet_statuses(timeout)[outlet]

    def toggle_outlet(self, outlet: int, state: str = "on") -> Optional[str]:
        """
        Toggle a specific outlet
        Args:
            outlet: ID of the outlet (from 1 to 8)
            state: The desired state of the outlets (on, off or reboot)

        Returns
            str: The final state of the outlets
        """
        if type(outlet) != int or outlet <= 0:
            raise ValueError("outlet must be a positive integer")
        if type(state) != str or state not in self.available_cmd:
            raise ValueError(
                f"state must be one of {self.available_cmd.keys()}"
            )

        outlet_status = "".join(
            "0" if i + 1 != outlet else "1" for i in range(8)
        )
        outlet_status += "0000000000000000"
        if state == "off":
            uri = "offs.cgi?led=" + outlet_status
        elif state == "on":
            uri = "ons.cgi?led=" + outlet_status
        elif state == "reboot":
            uri = "offon.cgi?led=" + outlet_status
        else:
            raise ValueError(
                f"State {state} is not in {self.available_cmd.keys()}"
            )

        r = requests.post(
            self.ip + uri,
        )
        if r.status_code != 200:
            raise Exception
        else:
            return state

    def toggle_all_outlets(self, state: str = "on") -> Optional[str]:
        """
        Toggles all outlets
        Args:
            state: The desired state of the outlets (on, off or reboot)

        Returns
            str: The final state of the outlets
        """
        if type(state) != str or state not in self.available_cmd:
            raise ValueError(
                f"state must be one of {self.available_cmd.keys()}"
            )
        outlet_status = "".join("1" for _ in range(8))
        outlet_status += "0000000000000000"

        if state == "off":
            uri = "offs.cgi?led=" + outlet_status
        elif state == "on":
            uri = "ons.cgi?led=" + outlet_status
        elif state == "reboot":
            uri = "offon.cgi?led=" + outlet_status
        else:
            raise ValueError(
                f"State {state} is not in {self.available_cmd.keys()}"
            )
        r = requests.post(
            self.ip + uri,
        )
        if r.status_code != 200:
            return None
        else:
            return state

    def get_all_names(self) -> List[str]:
        """
        Returns the name of all outlets

        Returns
        List str : The name of all outlets
        """
        r = requests.get(
            self.ip + "Getname.xml",
        )
        if r.status_code != 200:
            raise Exception
        else:
            data = xmltodict.parse(r.text)
            values = data["response"].values()
            return [name.split(",")[0] for name in values]

    def get_name(self, outlet: int) -> Optional[str]:
        """
        Returns the name of an outlet
        Args:
            outlet: ID of the outlet (from 1 to 8)

        Returns
        str : The name of the desired outlet
        """
        return self.get_all_names()[int(outlet) - 1]

    def set_name(self, outlet: int, name: str) -> Optional[str]:
        """Sets the name of an outlet

        Args:
            outlet: the outlet number
            name: the name to set (under 32 characters)
        """
        uri = "names1.cgi?led=0,"
        outlet_names = self.get_all_names()
        for num_outlet in range(1, len(outlet_names) + 1):
            if num_outlet != outlet:
                uri += outlet_names[num_outlet - 1].replace(" ", "%20") + ','
            else:
                uri += name.replace(" ", "%20") + ','
        r = requests.post(
            self.ip + uri,
        )

        if r.status_code != 200:
            return r.text.strip()
        else:
            return f"Successfully renamed outlet {outlet} to {name}"
