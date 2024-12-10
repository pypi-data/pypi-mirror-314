#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
import json
import sys

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
from typing import Any, List, Optional, Union

import requests


class PDUControlNetIO:
    """Class used to control the NetIO 4C PDU from the LU lab"""

    def __init__(self, ip: str, user: str = "admin", password: str = "admin"):
        self.ip = f"http://{user}:{password}@{ip}/"

    available_cmd = {
        "off": 0,
        "on": 1,
        "reboot": 2,
    }
    available_cmd_reverse = {
        0: "off",
        1: "on",
        2: "reboot",
    }

    def get_total_outlets(self) -> Optional[int]:
        """Returns the number of outlets"""
        r = requests.get(
            self.ip + "netio.json",
        )
        if r.status_code != 200:
            return None

        data = json.loads(r.text)
        return len(data.get("Outputs"))

    def get_all_outlet_statuses(self, timeout=None) -> Optional[List[str]]:
        """
        Returns the state of all the outlets
        Returns:
            List[str]: List containing the state of all outlets
        """
        r = requests.get(
            self.ip + "netio.json",
            timeout=timeout
        )
        if r.status_code != 200:
            return None
        data = json.loads(r.text)
        status = [output["State"] for output in data["Outputs"]]
        return [self.available_cmd_reverse[int(s)] for s in status]

    def get_outlet_status(self, outlet: int = 1, timeout=None
                          ) -> Optional[str]:
        """
        Returns the state of a specific outlet
        Args:
            outlet: ID of the outlet (from 1 to 4)
            timeout: max time without answer

        Returns:
            str: State of the desired outlet
        """
        return self.get_all_outlet_statuses(timeout)[outlet - 1]

    def toggle_outlet(self, outlet: int, state: str = "on") -> Optional[str]:
        """
        Toggle a specific outlet
        Args:
            outlet: ID of the outlet (from 1 to 4)
            state: The desired state of the outlets (on, off or reboot)

        Returns:
            str: The final state of the outlets
        """
        if type(state) is not str or state not in self.available_cmd:
            raise ValueError(
                f"state must be one of {self.available_cmd.keys()}"
            )

        r = requests.post(
            self.ip + "netio.json",
            data=json.dumps(
                {'Outputs': [{
                    "ID": outlet,
                    "Action": self.available_cmd.get(state)}]})
        )
        if r.status_code != 200:
            return f"request returned error {r.status_code}"
        return state

    def toggle_all_outlets(self, state: str = "on") -> Optional[str]:
        """
        Toggles all outlets
        Args:
            state: The desired state of the outlets (on, off or reboot)

        Returns:
            str: The final state of the outlets
        """
        if type(state) is not str or state not in self.available_cmd:
            raise ValueError(
                f"state must be one of {self.available_cmd.keys()}"
            )

        r = requests.post(
            self.ip + "netio.json",
            data=json.dumps(
                {'Outputs':
                 [{"ID": i, "Action": self.available_cmd.get(state)}
                  for i in range(1, self.get_total_outlets() + 1)], }

            )
        )
        if r.status_code != 200:
            return None

        return state

    def get_all_names(self) -> Union[str, List[Any]]:
        """
        Returns the name of all outlets

        Returns:
        List str : The name of all outlets
        """
        r = requests.get(
            self.ip + "netio.json",
        )
        if r.status_code != 200:
            return f"request returned error {r.status_code}"

        data = json.loads(r.text)
        return [output["Name"] for output in data["Outputs"]]

    def get_name(self, outlet: int) -> Optional[str]:
        """
        Returns the name of an outlet
        Args:
            outlet: ID of the outlet (from 1 to 4)

        Returns:
        str : The name of the desired outlet
        """
        return self.get_all_names()[int(outlet) - 1]

    def set_name(self, outlet: int, name: str) -> None:
        """Sets the name of an outlet

        Args:
            outlet: the outlet number
            name: the name to set (under 32 characters)
        """
        print(f"PDU does not support renaming via pducontrol. "
              f"Use the WebUI : {self.ip}")
        sys.exit(127)
