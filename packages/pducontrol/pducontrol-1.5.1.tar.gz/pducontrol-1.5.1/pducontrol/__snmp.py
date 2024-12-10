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

import subprocess
from dataclasses import dataclass
from typing import Optional, Union


class SNMPClient:
    _version_args_template = {
        'v1v2': '-c {community}',
        'v3': '-u {user} -a {auth} -x {priv} -A {authpass} '
              '-X {privpass} -l {authlevel}',
    }

    # Valid snmpset value types
    snmpset_value_types = (
        'i', 'u', 't', 'a', 'o', 's', 'x', 'd', 'b', 'U', 'I', 'F', 'D'
    )
    snmp_versions = ('1', '2c', '3')

    @dataclass
    class V3Args:
        """Internal SNMP class to hold SNMPv3-specific configuration"""

        user: str = 'user'
        authlevel: str = 'authPriv'
        auth: str = 'MD5'
        priv: str = 'DES'
        authpass: str = ''
        privpass: str = ''

    @dataclass
    class V1V2Args:
        """Internal SNMP class to hold SNMPv1/2c-specific configuration"""

        community: str = 'private'

    def __init__(self, ip: str, version: str, *, timeout: int = 10) -> None:
        if version not in self.snmp_versions:
            raise ValueError("SNMP version must be one of '1', '2c', or '3'")

        self.ip = ip
        self.version = version
        self.timeout = timeout
        self.version_args = {
            'v1v2': self.V1V2Args(),
            'v3': self.V3Args()
        }
        self._cli_args = ''
        self.__gen_version_cmd_args(version='v3' if '3' in version else 'v1v2')

    def set_ip(self, ip: int) -> None:
        """Sets the IP address to target SNMP requests to

        Keyword Arguments:
        ip -- The address of the target device
        """
        if type(ip) != str:
            raise ValueError(
                "ip must a string in standard ipv4 format '192.168.1.100'"
            )
        self.ip = ip

    def set_version(self, version: int) -> None:
        """Sets the SNMP version of the requests

        Keyword Arguments:
        version -- SNMP version of the request ('1', '2c', or '3')
        """
        if version not in self.snmp_versions:
            raise ValueError("version must be either '1', '2c', or '3'")
        self.version = version

    def __gen_version_cmd_args(self, version: str) -> None:
        self._cli_args = self._version_args_template[version].format(
            **self.version_args[version].__dict__
        )

    def __gen_snmpwalk_cmd(self, oid: str) -> str:
        """Snmpwalk command to query the device

        Keyword Arguments:
        oid -- The SNMP object identifier to query

        Returns:
        A string representing the whole snmpwalk query
        """
        return f"snmpwalk -v {self.version} -t {self.timeout} " \
               f"{self._cli_args} {self.ip} {oid}"

    def __gen_snmpset_cmd(self, oid: str, value_type: str, value: str) -> str:
        """Snmpset command to write to the device

        Keyword Arguments:
        oid -- The SNMP object identifier to query
        value_type -- The type of the value being written to the device
                      (e.g. integer, string, etc..)
        value -- The value being written to the device

        Returns:
        A string representing the whole snmpget query
        """
        if value_type not in self.snmpset_value_types:
            raise ValueError(
                f"Valid snmpset value types are {self.snmpset_value_types}"
            )

        return f"snmpset -v {self.version} -t {self.timeout} " \
               f"{self._cli_args} {self.ip} {oid} {value_type} {value}"

    def snmpwalk(self, oid: str, timeout=None) -> Optional[str]:
        """Snmpwalk query to the device

        Keyword Arguments:
        oid -- The SNMP object identifier to query

        Returns:
        A string representing the output of the snmpwalk query or None
        if an error occured
        """
        cmd = self.__gen_snmpwalk_cmd(oid=oid)
        result = subprocess.run(
            args=cmd.split(), capture_output=True, check=True, timeout=timeout,
        )

        return result.stdout.decode()

    def snmpset(self, oid: str, value_type: str, value: str) -> Optional[str]:
        """Snmpset query to the device

        Keyword Arguments:
        oid -- The SNMP object identifier to query
        value_type -- The type of the value being written to the device
                      (e.g. integer, string, etc..)
        value -- The value being written to the device

        Returns:
        A string representing the output of the snmpset query or None
        if an error occured
        """
        cmd = self.__gen_snmpset_cmd(
            oid=oid, value_type=value_type, value=value
        )
        result = subprocess.run(
            args=cmd.split(), capture_output=True, check=True
        )

        return result.stdout.decode()

    def parse_by_type(self, line: str, value_type: str) -> Union[int, str]:
        """Parser for snmpwalk/set return values based on value type

        Keyword Arguments:
        line -- The snmpwalk/set return value
        value_type -- The type of the value being written to the device
                      (e.g. integer, string, etc..)

        Returns:
        The parsed value. Currently either an integer or string
        """
        if value_type not in self.snmpset_value_types:
            raise ValueError(
                f"Valid snmpset value types are {self.snmpset_value_types}"
            )

        if value_type == "i":
            return int(line.rsplit(':', 1)[-1].strip())
        else:
            return line.rsplit(':', 1)[-1].strip()
