import xml.dom.minidom
import xml.etree.ElementTree as ET


class XMLGenerator:
    def __init__(
        self,
        host="app.diagrams.net",
        modified="2023-10-10T12:00:00.000Z",
        agent="python-script",
        etag="abcd1234",
        version="16.0.0",
        file_type="device",
    ):
        self.mxfile = ET.Element(
            "mxfile",
            {
                "host": host,
                "modified": modified,
                "agent": agent,
                "etag": etag,
                "version": version,
                "type": file_type,
            },
        )

    def add_diagram(self, diagram_id, name, graph_model_attrs):
        diagram = ET.SubElement(
            self.mxfile, "diagram", {"id": diagram_id, "name": name}
        )
        mxGraphModel = ET.SubElement(diagram, "mxGraphModel", graph_model_attrs)
        root = ET.SubElement(mxGraphModel, "root")
        # Default mxCells
        ET.SubElement(root, "mxCell", {"id": "0"})
        ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})
        return root

    def to_pretty_xml(self):
        rough_string = ET.tostring(self.mxfile, "utf-8")
        reparsed = xml.dom.minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")
        return pretty_xml

    def save_to_file(self, filename):
        pretty_xml = self.to_pretty_xml()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(pretty_xml)
