"""class-based cabling topography layout generator with physical port aggregation """


# ==============================================================================
# 1. OPTICS SPECIFICATION PROPERTY EXTRACTOR CLASS
# ==============================================================================
class CableSpecs:
    """
    Analyzes raw SFP hardware description strings to contextually extract
    and map individual physical media layer properties.
    """
    def __init__(self, sfp_type_str):
        self.sfp = str(sfp_type_str).upper().strip() if sfp_type_str else 'MISSING OPTIC'
        
        # Populate all derived traits immediately using explicit, localized methods
        self.medium = self.derive_medium()
        self.speed = self.derive_speed()
        self.cable_type = self.derive_cable_type()
        self.color = self.derive_color()

    def derive_medium(self):
        """Isolates the core physical cable medium profile layer."""
        if self.sfp in ['MISSING OPTIC', 'MISSING REMOTE FILE']:
            return "Unknown Medium"
        if any(x in self.sfp for x in ['DAC', 'TWINAX', 'PASSIVE COPPER', '10G-SFPP-CU']):
            return "Direct-Attach Copper (DAC)"
        if any(x in self.sfp for x in ['-T', '10G-T', 'COPPER', 'RJ45', '1000BASE-T']):
            return "Copper (Cat6/6A)"
        if any(x in self.sfp for x in ['LR', 'LX', 'LH', 'EX', 'ZX', 'ER', 'ZR', 'SR', 'SX', 'FX', 'FIBER', 'OPTIC', 'QSFP']):
            return "Fiber-Optic"
        return "Unknown Medium"

    def derive_speed(self):
        """Captures the active operational link bandwidth capacity."""
        if self.sfp in ['MISSING OPTIC', 'MISSING REMOTE FILE']:
            return 'Unknown Speed'

        # 100G
        if any(x in self.sfp for x in ['100G', 'QSFP28']):
            return '100Gbps'

        # 40G
        if any(x in self.sfp for x in ['40G', 'QSFP+']):
            return '40Gbps'

        # 25G
        if any(x in self.sfp for x in ['25G', 'SFP28']):
            return '25Gbps'

        # 10G
        if any(x in self.sfp for x in ['10G', 'SFP+']):
            return '10Gbps'

        # 1G
        if any(x in self.sfp for x in ['1000BASE', '1G', 'SX', 'LX']):
            return '1Gbps'

        return 'Unknown Speed'

    def derive_cable_type(self):
        """Maps out the exact physical patch cord connector type."""
        if self.sfp in ['MISSING OPTIC', 'MISSING REMOTE FILE']:
            return "Unknown Cable Type"
        if any(x in self.sfp for x in ['LR', 'LX', 'LH', 'EX', 'ZX', 'ER', 'ZR']):
            return "Single-Mode Fiber (SMF)"
        if any(x in self.sfp for x in ['SR', 'SX', 'FX']):
            return "Multi-Mode Fiber (MMF)"
        if any(x in self.sfp for x in ['DAC', 'TWINAX']):
            return "Direct-Attach Twinax Cable"
        if any(x in self.sfp for x in ['1000BASE-T', '100BASE-T', '1GBASE-T', 'RJ45']):
            return "RJ45 Copper Patch Cable"


    def derive_color(self):
        """
        Returns recommended visual identification color
        for patching documentation purposes.

        This is NOT necessarily the actual cable jacket color.
        """
        if self.medium == "Copper (Cat6/6A)":
            return "Brown"

        if self.medium == "Direct-Attach Copper (DAC)":
            return "Black"

        if self.speed == "1Gbps":
            return "Green"

        if self.speed == "10Gbps":
            return "Blue"

        if self.speed == "25Gbps":
            return "Purple"

        if self.speed == "40Gbps":
            return "Orange"

        if self.speed == "100Gbps":
            return "Red"

        return "Grey"

# ===================================================================================
if __name__ == "__main__":
    pass
# ===================================================================================
