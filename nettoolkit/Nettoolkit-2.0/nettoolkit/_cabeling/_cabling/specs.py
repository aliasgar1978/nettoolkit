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
        if any(x in self.sfp for x in ['-T', '10G-T', 'COPPER', 'RJ45', '1000BASE-T']):
            return "Copper (Cat6/6A)"
        if any(x in self.sfp for x in ['DAC', 'TWINAX', 'PASSIVE COPPER', '10G-SFPP-CU']):
            return "Direct-Attach Copper (DAC)"
        if any(x in self.sfp for x in ['LR', 'LX', 'LH', 'EX', 'ZX', 'ER', 'ZR', 'SR', 'SX', 'FX', 'FIBER', 'OPTIC', 'QSFP']):
            return "Fiber-Optic"
        return "Unknown Medium"

    def derive_speed(self):
        """Captures the active operational link bandwidth capacity."""
        if self.sfp in ['MISSING OPTIC', 'MISSING REMOTE FILE']:
            return "Unknown Speed"
        if any(x in self.sfp for x in ['10G', 'LR', 'SR', 'ER', 'ZR']):
            return "10Gbps"
        if any(x in self.sfp for x in ['QSFP', '40G']):
            return "40Gbps"
        if '100G' in self.sfp:
            return "100Gbps"
        if any(x in self.sfp for x in ['1G', 'SX', 'LX', 'GIGABIT', '1000BASE']):
            return "1Gbps"
        return "1Gbps (Fallback)"

    def derive_cable_type(self):
        """Maps out the exact physical patch cord connector type."""
        if self.sfp in ['MISSING OPTIC', 'MISSING REMOTE FILE']:
            return "Unknown Cable Type"
        if "COPPER" in self.medium.upper():
            return "RJ45 Copper Patch Cable"
        if "DIRECT-ATTACH" in self.medium.upper():
            return "Direct-Attach Twinax Cable"
        if "QSFP" in self.sfp or "40G" in self.sfp:
            return "MPO to 4xLC Multi-Mode Breakout Fiber"
        if any(x in self.sfp for x in ['LR', 'LX', 'LH', 'EX', 'ZX', 'ER', 'ZR']):
            return "LC to LC Single-Mode Fiber (SMF)"
        if any(x in self.sfp for x in ['SR', 'SX', 'FX']):
            return "LC to SC Multi-Mode Fiber (MMF)" if 'SC' in self.sfp else "LC to LC Multi-Mode Fiber (MMF)"
        return "LC to LC Fiber Patch Cable" if "FIBER" in self.medium.upper() else "Verify Physical Slot Optic"

    def derive_color(self):
        """Assigns the standardized physical cable jacket or latch clip color coding."""
        if self.sfp in ['MISSING OPTIC', 'MISSING REMOTE FILE']:
            return "Unknown Color"
        if "COPPER" in self.medium.upper():
            return "Black"
        if "DIRECT-ATTACH" in self.medium.upper():
            return "Black / Twinax Grey"
        if any(x in self.sfp for x in ['LR', 'LX', 'LH', 'EX', 'ZX', 'ER', 'ZR']):
            return "Yellow"
        if any(x in self.sfp for x in ['SR', 'SX', 'FX', 'QSFP']):
            if any(x in self.sfp for x in ['OM3', '10GBASE-SR', 'QSFP', '40G']):
                return "Sky Blue (Aqua)"
            return "Orange"
        return "Verify Physical Cable Media"

# ===================================================================================
if __name__ == "__main__":
    pass
# ===================================================================================
