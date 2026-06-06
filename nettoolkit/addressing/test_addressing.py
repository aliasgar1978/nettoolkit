import inspect
import unittest

from nettoolkit.addressing import sorted_v4_addresses, sort_by_size
# from addressing import IPv4, sorted_v4_addresses, sort_by_size


class TestIPv4Subnet(unittest.TestCase):
    """Unit tests for IPv4 subnet properties and operations across various subnet sizes."""

    prefixes = ["10.10.8.0/23", "10.10.10.0/23"]
    unsorted_list_of_subnets = [
        "10.10.10.0/25",
        "10.10.2.0/24",
        "10.20.10.0/24",
        "10.10.5.0/24",
        "10.10.10.128/25",
        "10.1.10.0/24",
        "10.10.7.0/24",
        "10.10.1.0/24",
        "100.10.10.0/24",
        "192.168.10.0/24",
        "192.168.1.0/24",
        "172.16.10.0/24",
        "172.16.2.0/24",
    ]

    expected_sorted = [
        '10.1.10.0/24',
        '10.10.1.0/24',
        '10.10.2.0/24',
        '10.10.5.0/24',
        '10.10.7.0/24',
        '10.10.10.0/25',
        '10.10.10.128/25',
        '10.20.10.0/24',
        '100.10.10.0/24',
        '172.16.2.0/24',
        '172.16.10.0/24',
        '192.168.1.0/24',
        '192.168.10.0/24',
    ]

    expected_sort_by_size = [
        '10.1.10.0/24',
        '10.10.1.0/24',
        '10.10.2.0/24',
        '10.10.5.0/24',
        '10.10.7.0/24',
        '10.20.10.0/24',
        '100.10.10.0/24',
        '172.16.2.0/24',
        '172.16.10.0/24',
        '192.168.1.0/24',
        '192.168.10.0/24',
        '10.10.10.0/25',
        '10.10.10.128/25',
    ]

    expected_custom_sorted = [
        '10.1.10.0/24',
        '10.10.10.128/25',
        '10.10.10.0/25',
        '10.10.7.0/24',
        '10.10.5.0/24',
        '10.10.2.0/24',
        '10.10.1.0/24',
        '10.20.10.0/24',
        '100.10.10.0/24',
        '172.16.10.0/24',
        '172.16.2.0/24',
        '192.168.10.0/24',
        '192.168.1.0/24',
    ]

    host_subnet = {
        'subnet': '202.144.115.206/32',
        'subnet_zero': '202.144.115.206',
        'broadcast_address': '202.144.115.206',
        'decmask': 32,
        'netmask': '255.255.255.255',
        'inverse_mask': '0.0.0.0',
        'version': 4,
        'ip_count': 1,
        'ipbinmask': '202.144.115.206 255.255.255.255',
        'ipdecmask': '202.144.115.206/32',
        'ipinvmask': '202.144.115.206 0.0.0.0',
        'expanded_subnet': '202.144.115.0/24',
        'network_number_int': 3398464462,
        'broadcast_number_int': 3398464462,
        'size': 1
    }
    class_c_subnet = {
        'subnet': '192.168.1.0/24',
        'subnet_zero': '192.168.1.0',
        'broadcast_address': '192.168.1.255',
        'decmask': 24,
        'netmask': '255.255.255.0',
        'inverse_mask': '0.0.0.255',
        'version': 4,
        'ip_count': 256,
        '5th_ip': '192.168.1.5',
        'ipbinmask': '192.168.1.0 255.255.255.0',
        'ipbinmask_5': '192.168.1.5 255.255.255.0',
        'ipdecmask': '192.168.1.0/24',
        'ipdecmask_5': '192.168.1.5/24',
        'ipinvmask': '192.168.1.0 0.0.0.255',
        'ipinvmask_5': '192.168.1.5 0.0.0.255',
        'expanded_subnet': '192.168.0.0/23',
        '4th_ip': '192.168.1.4',
        'first_5': ('192.168.1.0', '192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4'),
        'break_4': ('192.168.1.0/26', '192.168.1.64/26', '192.168.1.128/26', '192.168.1.192/26'),
        'network_number_int': 3232235776,
        'broadcast_number_int': 3232236031,
        'size': 256
    }
    class_b_subnet = {
        'subnet': '172.15.0.0/16',
        'subnet_zero': '172.15.0.0',
        'broadcast_address': '172.15.255.255',
        'decmask': 16,
        'netmask': '255.255.0.0',
        'inverse_mask': '0.0.255.255',
        'version': 4,
        'ip_count': 65536,
        '5th_ip': '172.15.0.5',
        'ipbinmask': '172.15.0.0 255.255.0.0',
        'ipbinmask_5': '172.15.0.5 255.255.0.0',
        'ipdecmask': '172.15.0.0/16',
        'ipdecmask_5': '172.15.0.5/16',
        'ipinvmask': '172.15.0.0 0.0.255.255',
        'ipinvmask_5': '172.15.0.5 0.0.255.255',
        '4th_ip': '172.15.0.4',
        'first_5': ('172.15.0.0', '172.15.0.1', '172.15.0.2', '172.15.0.3', '172.15.0.4'),
        'break_4': ('172.15.0.0/18', '172.15.64.0/18', '172.15.128.0/18', '172.15.192.0/18'),
        'expanded_subnet': '172.12.0.0/14',
        'network_number_int': 2886664192,
        'broadcast_number_int': 2886729727,
        'size': 65536
    }
    class_a_subnet = {
        'subnet': '9.0.0.0/8',
        'subnet_zero': '9.0.0.0',
        'broadcast_address': '9.255.255.255',
        'decmask': 8,
        'netmask': '255.0.0.0',
        'inverse_mask': '0.255.255.255',
        'version': 4,
        'ip_count': 16777216,
        '5th_ip': '9.0.0.5',
        'ipbinmask': '9.0.0.0 255.0.0.0',
        'ipbinmask_5': '9.0.0.5 255.0.0.0',
        'ipdecmask': '9.0.0.0/8',
        'ipdecmask_5': '9.0.0.5/8',
        'ipinvmask': '9.0.0.0 0.255.255.255',
        'ipinvmask_5': '9.0.0.5 0.255.255.255',
        '4th_ip': '9.0.0.4',
        'first_5': ('9.0.0.0', '9.0.0.1', '9.0.0.2', '9.0.0.3', '9.0.0.4'),
        'break_4': ('9.0.0.0/10', '9.64.0.0/10', '9.128.0.0/10', '9.192.0.0/10'),
        'expanded_subnet': '8.0.0.0/7',
        'network_number_int': 150994944,
        'broadcast_number_int': 167772159,
        'size': 16777216
    }

    def setUp(self):
        """Instantiate IPv4 objects for predefined subnet examples used across tests."""
        self.host_ip = IPv4(self.host_subnet['subnet'])
        self.class_c_ip = IPv4(self.class_c_subnet['subnet'])
        self.class_b_ip = IPv4(self.class_b_subnet['subnet'])
        self.class_a_ip = IPv4(self.class_a_subnet['subnet'])
        self.prefixes_v4_obj = [IPv4(_) for _ in self.prefixes]

    def test_obj_addition(self):
        """Verify that adding two IPv4 prefixes returns their correct aggregate prefix."""
        self.assertEqual(self.prefixes_v4_obj[0] + self.prefixes_v4_obj[1], "10.10.8.0/22")

    def test_subnet_zero(self):
        """Verify that subnet_zero returns the correct network address without the mask."""
        self.assertEqual(self.host_ip.subnet_zero(withMask=False), self.host_subnet['subnet_zero'])
        self.assertEqual(self.class_c_ip.subnet_zero(withMask=False), self.class_c_subnet['subnet_zero'])
        self.assertEqual(self.class_b_ip.subnet_zero(withMask=False), self.class_b_subnet['subnet_zero'])
        self.assertEqual(self.class_a_ip.subnet_zero(withMask=False), self.class_a_subnet['subnet_zero'])

    def test_broadcast_address(self):
        """Verify that broadcast_address returns the correct broadcast address without the mask."""
        self.assertEqual(self.host_ip.broadcast_address(withMask=False), self.host_subnet['broadcast_address'])
        self.assertEqual(self.class_c_ip.broadcast_address(withMask=False), self.class_c_subnet['broadcast_address'])
        self.assertEqual(self.class_b_ip.broadcast_address(withMask=False), self.class_b_subnet['broadcast_address'])
        self.assertEqual(self.class_a_ip.broadcast_address(withMask=False), self.class_a_subnet['broadcast_address'])

    def test_decmask(self):
        """Verify that the prefix length (decmask) matches expected values."""
        self.assertEqual(self.host_ip.decmask, self.host_subnet['decmask'])
        self.assertEqual(self.class_c_ip.decmask, self.class_c_subnet['decmask'])
        self.assertEqual(self.class_b_ip.decmask, self.class_b_subnet['decmask'])
        self.assertEqual(self.class_a_ip.decmask, self.class_a_subnet['decmask'])

    def test_netmask(self):
        """Verify that the netmask string matches expected values."""
        self.assertEqual(self.host_ip.binmask, self.host_subnet['netmask'])
        self.assertEqual(self.class_c_ip.binmask, self.class_c_subnet['netmask'])
        self.assertEqual(self.class_b_ip.binmask, self.class_b_subnet['netmask'])
        self.assertEqual(self.class_a_ip.binmask, self.class_a_subnet['netmask'])

    def test_inverse_mask(self):
        """Verify that the inverse mask string matches expected values."""
        self.assertEqual(self.host_ip.invmask, self.host_subnet['inverse_mask'])
        self.assertEqual(self.class_c_ip.invmask, self.class_c_subnet['inverse_mask'])
        self.assertEqual(self.class_b_ip.invmask, self.class_b_subnet['inverse_mask'])
        self.assertEqual(self.class_a_ip.invmask, self.class_a_subnet['inverse_mask'])

    def test_version(self):
        """Verify that the IP version is correctly reported as IPv4."""
        self.assertEqual(self.host_ip.version, self.host_subnet['version'])
        self.assertEqual(self.class_c_ip.version, self.class_c_subnet['version'])
        self.assertEqual(self.class_b_ip.version, self.class_b_subnet['version'])
        self.assertEqual(self.class_a_ip.version, self.class_a_subnet['version'])

    def test_host_count(self):
        """Verify that the total number of host addresses in each subnet matches expected sizes."""
        self.assertEqual(self.host_ip.ip_count, self.host_subnet['ip_count'])
        self.assertEqual(self.class_c_ip.ip_count, self.class_c_subnet['ip_count'])
        self.assertEqual(self.class_b_ip.ip_count, self.class_b_subnet['ip_count'])
        self.assertEqual(self.class_a_ip.ip_count, self.class_a_subnet['ip_count'])

    def test_n_thIP(self):
        """Verify nth IP address retrieval and index-access behavior for various subnets."""
        with self.assertRaises(Exception):
            self.host_ip.n_thIP(5, withMask=False)
            self.host_ip[4]
        self.assertEqual(self.class_c_ip.n_thIP(5, withMask=False), self.class_c_subnet['5th_ip'])
        self.assertEqual(self.class_b_ip.n_thIP(5, withMask=False), self.class_b_subnet['5th_ip'])
        self.assertEqual(self.class_a_ip.n_thIP(5, withMask=False), self.class_a_subnet['5th_ip'])
        self.assertEqual(self.class_c_ip[4], self.class_c_subnet['4th_ip'])
        self.assertEqual(self.class_b_ip[4], self.class_b_subnet['4th_ip'])
        self.assertEqual(self.class_a_ip[4], self.class_a_subnet['4th_ip'])

    def test_expand(self):
        """Verify that expanding a subnet to a broader mask returns the expected aggregate subnet."""
        self.assertEqual(self.host_ip.expand(24), self.host_subnet['expanded_subnet'])
        self.assertEqual(self.class_c_ip.expand(23), self.class_c_subnet['expanded_subnet'])
        self.assertEqual(self.class_b_ip.expand(14), self.class_b_subnet['expanded_subnet'])
        self.assertEqual(self.class_a_ip.expand(7), self.class_a_subnet['expanded_subnet'])

    def test_network_broadcast_size(self):
        """Verify network/broadcast numeric addresses and subnet size properties."""
        self.assertEqual(self.host_ip.network_number_int, self.host_subnet['network_number_int'])
        self.assertEqual(self.class_c_ip.network_number_int, self.class_c_subnet['network_number_int'])
        self.assertEqual(self.class_b_ip.network_number_int, self.class_b_subnet['network_number_int'])
        self.assertEqual(self.class_a_ip.network_number_int, self.class_a_subnet['network_number_int'])
        self.assertEqual(self.host_ip.broadcast_number_int, self.host_subnet['broadcast_number_int'])
        self.assertEqual(self.class_c_ip.broadcast_number_int, self.class_c_subnet['broadcast_number_int'])
        self.assertEqual(self.class_b_ip.broadcast_number_int, self.class_b_subnet['broadcast_number_int'])
        self.assertEqual(self.class_a_ip.broadcast_number_int, self.class_a_subnet['broadcast_number_int'])
        self.assertEqual(self.host_ip.size, self.host_subnet['size'])
        self.assertEqual(self.class_c_ip.size, self.class_c_subnet['size'])
        self.assertEqual(self.class_b_ip.size, self.class_b_subnet['size'])
        self.assertEqual(self.class_a_ip.size, self.class_a_subnet['size'])

    def test_ipbinmask_ipdecmask_ipinvmask(self):
        """Verify binary mask, decimal mask, and inverse mask representations with and without specific IP offsets."""
        self.assertEqual(self.host_ip.ipbinmask(), self.host_subnet['ipbinmask'])
        self.assertEqual(self.class_c_ip.ipbinmask(), self.class_c_subnet['ipbinmask'])
        self.assertEqual(self.class_b_ip.ipbinmask(), self.class_b_subnet['ipbinmask'])
        self.assertEqual(self.class_a_ip.ipbinmask(), self.class_a_subnet['ipbinmask'])
        with self.assertRaises(Exception):
            self.host_ip.ipbinmask(5)
        self.assertEqual(self.class_c_ip.ipbinmask(5), self.class_c_subnet['ipbinmask_5'])
        self.assertEqual(self.class_b_ip.ipbinmask(5), self.class_b_subnet['ipbinmask_5'])
        self.assertEqual(self.class_a_ip.ipbinmask(5), self.class_a_subnet['ipbinmask_5'])
        self.assertEqual(self.host_ip.ipdecmask(), self.host_subnet['ipdecmask'])
        self.assertEqual(self.class_c_ip.ipdecmask(), self.class_c_subnet['ipdecmask'])
        self.assertEqual(self.class_b_ip.ipdecmask(), self.class_b_subnet['ipdecmask'])
        self.assertEqual(self.class_a_ip.ipdecmask(), self.class_a_subnet['ipdecmask'])
        with self.assertRaises(Exception):
            self.host_ip.ipdecmask(5)
        self.assertEqual(self.class_c_ip.ipdecmask(5), self.class_c_subnet['ipdecmask_5'])
        self.assertEqual(self.class_b_ip.ipdecmask(5), self.class_b_subnet['ipdecmask_5'])
        self.assertEqual(self.class_a_ip.ipdecmask(5), self.class_a_subnet['ipdecmask_5'])
        self.assertEqual(self.host_ip.ipinvmask(), self.host_subnet['ipinvmask'])
        self.assertEqual(self.class_c_ip.ipinvmask(), self.class_c_subnet['ipinvmask'])
        self.assertEqual(self.class_b_ip.ipinvmask(), self.class_b_subnet['ipinvmask'])
        self.assertEqual(self.class_a_ip.ipinvmask(), self.class_a_subnet['ipinvmask'])
        with self.assertRaises(Exception):
            self.host_ip.ipinvmask(5)
        self.assertEqual(self.class_c_ip.ipinvmask(5), self.class_c_subnet['ipinvmask_5'])
        self.assertEqual(self.class_b_ip.ipinvmask(5), self.class_b_subnet['ipinvmask_5'])
        self.assertEqual(self.class_a_ip.ipinvmask(5), self.class_a_subnet['ipinvmask_5'])

    def test_get_slice(self):
        """Verify slice access returns the first N hosts in a subnet and invalid slices raise exceptions."""
        with self.assertRaises(Exception):
            self.host_ip[0:5]
        self.assertEqual(self.class_c_ip[0:5], self.class_c_subnet['first_5'])
        self.assertEqual(self.class_b_ip[0:5], self.class_b_subnet['first_5'])
        self.assertEqual(self.class_a_ip[0:5], self.class_a_subnet['first_5'])

    def test_subnet_break(self):
        """Verify subnet division into smaller subnets and invalid division raises ValueError."""
        with self.assertRaises(ValueError):
            _ = self.host_ip / 4
        self.assertEqual(self.class_c_ip / 4, self.class_c_subnet['break_4'])
        self.assertEqual(self.class_b_ip / 4, self.class_b_subnet['break_4'])
        self.assertEqual(self.class_a_ip / 4, self.class_a_subnet['break_4'])

    def test_sorted_v4_addresses(self):
        """Verify sorted_v4_addresses orders a list of unsorted IPv4 subnets correctly."""
        self.assertEqual(
            sorted_v4_addresses(self.unsorted_list_of_subnets), 
            self.expected_sorted)
        self.assertEqual(
            sorted_v4_addresses(self.unsorted_list_of_subnets, ascending=False),
            list(reversed(self.expected_sorted))
        )

    def test_sorted_v4_addresses_with_custom_ascending(self):
        """Verify sorted_v4_addresses accepts a custom ascending pattern for octets and prefix."""
        self.assertEqual(
            sorted_v4_addresses(self.unsorted_list_of_subnets, ascending=[True, True, False, False, True]),
            self.expected_custom_sorted
        )

    def test_sort_by_size(self):
        """Verify sort_by_size orders a list of unsorted IPv4 subnets by size."""
        self.assertEqual(
            sort_by_size(self.unsorted_list_of_subnets),
            self.expected_sort_by_size
        )



if __name__ == '__main__':
    unittest.main()
