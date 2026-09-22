

class Topology():

    def set_remarks(self, remarks):
        if isinstance(remarks, (str, int, float)):
            self.remarks = str(remarks)
        elif isinstance(remarks, (list, set, tuple)):
            self.remarks = "\n".join(remarks)
        elif isinstance(remarks, dict):
            self.remarks = "\n".join(f"{k}: {v}" for k, v in remarks.items())

    def additional_remarks(self, **kwargs):
        self.remarks +=  "\n" + "\n".join(f"{k}: {v}" for k, v in self.remarks.items())
