from pathlib import Path
import win32com.client as win32


class VisioRenderer:
    def __init__(self, visible: bool = True):
        self.app = win32.DispatchEx("Visio.Application")
        self.app.Visible = visible
        self.document = self.app.Documents.Add("")
        self.shape_index = {}

    def add_page(self, name: str):
        page = self.document.Pages.Add()
        page.Name = name
        return page

    def add_device(self, page, node, x: float, y: float):
        shape = page.DrawRectangle(
            x - 0.8,
            y - 0.45,
            x + 0.8,
            y + 0.45,
        )

        shape.Text = (
            f"{node.hostname}\n"
            f"{node.model or 'Unknown model'}\n"
            f"{node.loopback_ipv4 or ''}"
        )

        shape.NameU = f"NODE_{node.node_id}"
        self.shape_index[node.node_id] = shape
        self._set_node_shape_data(shape, node)

        return shape

    def connect_devices(self, page, edge):
        source = self.shape_index[edge.source_node]
        target = self.shape_index[edge.target_node]

        connector = page.Drop(
            self.app.ConnectorToolDataObject,
            0,
            0,
        )

        connector.CellsU("BeginX").GlueTo(
            source.CellsU("PinX")
        )
        connector.CellsU("EndX").GlueTo(
            target.CellsU("PinX")
        )

        connector.Text = (
            f"{edge.source_port}\n"
            f"{edge.target_port}\n"
            f"{edge.speed or ''}"
        )

        self._style_edge(connector, edge)
        return connector

    def save(self, output_file: Path):
        self.document.SaveAs(str(output_file.resolve()))

    def close(self):
        self.document.Close()
        self.app.Quit()

    def _set_node_shape_data(self, shape, node):
        # Add Visio Shape Data fields in the production version.
        pass

    def _style_edge(self, connector, edge):
        if edge.status == "up":
            connector.CellsU("LineColor").FormulaU = "RGB(0,176,80)"
        elif edge.status in {"down", "administratively down"}:
            connector.CellsU("LineColor").FormulaU = "RGB(192,0,0)"
            connector.CellsU("LinePattern").FormulaU = "2"
        else:
            connector.CellsU("LineColor").FormulaU = "RGB(127,127,127)"