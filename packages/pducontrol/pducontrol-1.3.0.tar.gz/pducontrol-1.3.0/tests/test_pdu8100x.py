import unittest
import ipaddress
import random
from unittest.mock import Mock
from pducontrol.__pdu8100x import PDU8100X


class PDU8100XTests(unittest.TestCase):
    """ Test class for the PDU8100X network-controlled power switch.

    Tests:
        SNMP specific tests:
        - test_snmpwalk_syntax: Checks if the snmpwalk command is structured
          correctly
        - test_snmpset_syntax: Checks if the snmpset command is structured
          correctly
        Instrument specific tests:
        - test_set_IP: Tests if the the target IP changes after setting the IP
        - test_set_version: Tests if the the SNMP version changes after setting
          the version
        - test_get_total_outlets: Tests if the function behaves as expected
          given no error & errors
        - test_get_outlet_status: Tests if the function behaves as expected
          given no error & errors
        - test_get_all_outlet_statuses: Tests if the function behaves as
          expected given no error & errors
        - test_toggle_outlet: Tests if the function behaves as expected given
          no error & errors
        - test_toggle_all_outlets: Tests if the function behaves as expected
          given no error & errors
    """

    @classmethod
    def setUpClass(cls):
        cls.test_ip = str(ipaddress.IPv4Address(random.randint(0, 2 ** 32)))
        cls.test_version = '1'
        cls.test_pdu8100x = PDU8100X(ip=cls.test_ip, version=cls.test_version)
        cls.test_pdu8100x.snmpwalk = Mock()
        cls.test_pdu8100x.snmpset = Mock()

    def test_set_ip(self):
        self.test_ip = str(ipaddress.IPv4Address(random.randint(0, 2 ** 32)))
        self.test_pdu8100x.set_ip(self.test_ip)
        self.assertEqual(self.test_pdu8100x.ip, self.test_ip)

    def test_set_version(self):
        self.test_version = '2c'
        self.test_pdu8100x.set_version(self.test_version)
        self.assertEqual(self.test_pdu8100x.version, '2c')

    def test_get_total_outlets(self):
        pdu = self.test_pdu8100x
        rand_total_outlets = random.choice((2, 4, 8, 16))
        pdu.snmpwalk.return_value = f"Integer: {rand_total_outlets}"

        self.assertEqual(pdu.get_total_outlets(), rand_total_outlets)

    def test_get_outlet_status(self):
        status_dict = self.test_pdu8100x.oid_status_outlet_state_results
        rand_status = random.choice(list(status_dict.keys()))
        self.test_pdu8100x.snmpwalk.return_value = f"Integer: {rand_status}"

        self.assertEqual(
            self.test_pdu8100x.get_outlet_status(outlet=1),
            status_dict[rand_status]
        )

    def test_get_all_outlet_statuses(self):
        status_dict = self.test_pdu8100x.oid_status_outlet_state_results
        rand_total_outlets = random.choice((2, 4, 8, 16))
        expected_status_list = [
            random.choice(list(status_dict.keys()))
            for _ in range(rand_total_outlets)
        ]

        self.test_pdu8100x.snmpwalk.return_value = "\n".join(
            f"Integer: {status}" for status in expected_status_list
        )

        self.assertEqual(
            (self.test_pdu8100x.get_all_outlet_statuses()),
            [status_dict[status] for status in expected_status_list]
        )

    def test_toggle_outlet(self):
        pdu = self.test_pdu8100x
        ctrl_one_state_dict = pdu.oid_control_command_values
        readable_outlet_state = random.choice(list(ctrl_one_state_dict.keys()))

        pdu.snmpset.return_value = (
            f"Integer: {ctrl_one_state_dict[readable_outlet_state]}"
        )

        outlet_state = pdu.toggle_outlet(
            outlet=1, state=readable_outlet_state
        )

        self.assertIn(outlet_state, readable_outlet_state)

    def test_toggle_all_outlets(self):
        ctrl_all_state_dict = self.test_pdu8100x.oid_dev_command_values
        readable_outlet_state = random.choice(list(ctrl_all_state_dict.keys()))

        self.test_pdu8100x.snmpset.return_value = (
            f"Integer: {ctrl_all_state_dict[readable_outlet_state]}"
        )

        outlet_state = self.test_pdu8100x.toggle_all_outlets(
            state=readable_outlet_state
        )

        self.assertIn(outlet_state, readable_outlet_state)


if __name__ == "__main__":
    unittest.main()
