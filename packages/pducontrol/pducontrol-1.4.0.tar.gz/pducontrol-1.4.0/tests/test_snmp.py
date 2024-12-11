import ipaddress
import random
import unittest
from unittest.mock import Mock, patch

from pducontrol.__snmp import SNMPClient


class SNMPClientTests(unittest.TestCase):
    """Test class for the SNMP Client class"""

    @classmethod
    def setUpClass(cls):
        """Hook method for setting up class fixture before running tests"""
        cls.test_ip = str(ipaddress.IPv4Address(random.randint(0, 2 ** 32)))

    def __get_snmp_client(self):
        return SNMPClient(ip=self.test_ip, version='1')

    def __mock_subprocess_run(self, response_stdout):
        """Returns a callable that Mock will call when 'subprocess.run'
        is called.
        """

        def response(args, **kwargs):
            """Returns a mock object with attribute 'stdout'"""
            return Mock(**{'stdout': response_stdout})

        return response

    @patch('pducontrol.__snmp.subprocess')
    def test_snmpwalk_syntax(self, mock_subprocess) -> None:
        """Tests snmpwalk command syntax"""
        test_client = self.__get_snmp_client()
        mock_subprocess.run.side_effect = self.__mock_subprocess_run(
            response_stdout='INTEGER: 6'.encode()
        )
        snmp_oid = "1.3.7.1.1337.1.2.4.4.1.0"

        test_client.snmpwalk(snmp_oid)
        snmpwalk_cmd = " ".join(mock_subprocess.run.call_args[1]["args"])

        self.assertIn('snmpwalk', snmpwalk_cmd)
        self.assertIn(f"-v {test_client.version}", snmpwalk_cmd)
        self.assertIn(test_client.ip, snmpwalk_cmd)
        self.assertIn(snmp_oid, snmpwalk_cmd)

    @patch('pducontrol.__snmp.subprocess')
    def test_snmpset_syntax(self, mock_subprocess) -> None:
        """Tests snmpset command syntax"""
        test_client = self.__get_snmp_client()
        mock_subprocess.run.side_effect = self.__mock_subprocess_run(
            response_stdout='INTEGER: 6'.encode()
        )
        snmp_oid = "1.3.7.1.1337.1.2.4.4.1.0"
        snmp_value_type = "i"
        snmp_value = "2"

        test_client.snmpset(snmp_oid, snmp_value_type, snmp_value)
        snmpset_cmd = " ".join(mock_subprocess.run.call_args[1]["args"])

        self.assertIn('snmpset', snmpset_cmd)
        self.assertIn(f"-v {test_client.version}", snmpset_cmd)
        self.assertIn(test_client.ip, snmpset_cmd)
        self.assertIn(snmp_oid, snmpset_cmd)
        self.assertIn(f"{snmp_value_type} {snmp_value}", snmpset_cmd)
