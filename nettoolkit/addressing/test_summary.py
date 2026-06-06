import inspect
import unittest

from nettoolkit.addressing.addressing import IPv4
from nettoolkit.addressing import isSubset
from nettoolkit.addressing.summary import calc_summmaries, Subnet_Spare, Aggregate

# from addressing import IPv4, isSubset
# from summary import Aggregate, calc_summmaries, Subnet_Spare



class TestIPv4Prefix(unittest.TestCase):
    """Unit tests for IPv4 prefix manipulation and aggregation behavior."""

    networks = (
        '10.10.0.0/24', '10.10.1.0/24', '10.20.6.0/23',
        '10.10.2.0/23', '10.20.4.0/23', '10.10.4.0/22'
    )
    is_in_check_prefixes = [
        ("192.168.1.1", "192.168.1.0/24", True),
        ("192.168.1.0", "192.168.1.0/24", True),
        ("192.168.1.255", "192.168.1.0/24", True),
        ("10.10.10.10", "10.10.8.0/23", False),
        ("10.10.9.255", "10.10.8.0/23", True),
        ("10.10.8.0/23", "10.10.8.0/22", True),
        ("10.10.9.0/24", "10.10.8.0/23", True),
        ("10.10.8.0/23", "10.10.9.0/24", False),
        ("192.168.1.1", "192.168.1.1/32", True),
        ("192.168.1.2", "192.168.1.1/32", False),
    ]
    is_not_in_check_prefixes  = [
        ('192.168.0.0/23', 
         ['192.168.0.160/27', '192.168.1.64/27', '10.10.10.0/24', '224.0.0.0/24'], 
         ['192.168.0.0/25', '192.168.0.128/27', '192.168.0.192/26', '192.168.1.0/26', '192.168.1.96/27', '192.168.1.128/25'],  
        ),
        ('10.10.0.0/22',
         [ '10.10.1.128/25', '10.10.1.0/25', '172.16.0.0/16'],
         ['10.10.0.0/24', '10.10.2.0/23'],
        ),
        ('192.168.2.0/24',
         ['192.168.2.0/26', '192.168.2.64/26', '192.168.2.192/26', '192.168.3.0/24'],
         ['192.168.2.128/26'],
        ),
    ]

    def setUp(self):
        """Prepare IPv4 prefix objects and aggregation helper for tests."""
        self.aggs = Aggregate(self.networks)

    def test_object_aggregations(self):
        """Verify that prefix aggregation returns expected prefixes, summaries, and IPv4 aggregate objects."""
        self.assertEqual(
            self.aggs.prefixes,
            ['10.10.0.0/24', '10.10.1.0/24', '10.10.2.0/23', '10.10.4.0/22', '10.20.4.0/23', '10.20.6.0/23']
        )
        self.assertEqual(self.aggs.summaries, ['10.10.0.0/21', '10.20.4.0/22'])
        self.assertEqual(
            self.aggs.aggregates,
            [IPv4('10.10.0.0/21'), IPv4('10.20.4.0/22')]
        )


    def test_prefix_isincheck(self):
        """Verify that isSubset correctly identifies whether IPs or prefixes are contained within a given IPv4 prefix."""
        for ip, prefix, result in self.is_in_check_prefixes:
            self.assertEqual(isSubset(ip, prefix), result)

    def test_prefix_isnotincheck(self):
        """Verify that isSubset correctly identifies whether prefixes are NOT contained within a given IPv4 prefix."""
        for supernet, prefixes, missing_prefixes in self.is_not_in_check_prefixes:
            SS = Subnet_Spare(supernet, prefixes=prefixes)
            self.assertEqual(SS.unused_prefixes(), missing_prefixes)

    def test_calc_summmaries(self):
        """Verify that calc_summmaries returns the correct summary prefixes for a given list of IPv4 prefixes."""
        summaries = calc_summmaries(min_subnet_size=19, prefixes=self.networks)
        self.assertEqual(summaries, ['10.10.0.0/19', '10.20.0.0/19'])



if __name__ == '__main__':
    unittest.main()
