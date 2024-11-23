import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


class DiagramElement(ABC):
    def __init__(self, element_id, parent_id):
        self.element_id = element_id
        self.parent_id = parent_id

    @abstractmethod
    def to_xml(self):
        pass


class Shape(DiagramElement):
    def __init__(self, element_id, parent_id, value, style, x, y, width, height):
        super().__init__(element_id, parent_id)
        self.value = value or ""
        self.style = style or ""
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def to_xml(self):
        shape_cell = ET.Element(
            "mxCell",
            {
                "id": str(self.element_id) if self.element_id else "",
                "value": self.value,
                "style": self.style,
                "vertex": "1",
                "parent": str(self.parent_id) if self.parent_id else "",
            },
        )
        geometry = ET.SubElement(
            shape_cell,
            "mxGeometry",
            {
                "x": str(self.x) if self.x is not None else "0",
                "y": str(self.y) if self.y is not None else "0",
                "width": str(self.width) if self.width is not None else "0",
                "height": str(self.height) if self.height is not None else "0",
                "as": "geometry",
            },
        )
        geometry.set("relative", "0")
        return shape_cell


class Connector(DiagramElement):
    def __init__(self, element_id, parent_id, source_id, target_id, style=None):
        super().__init__(element_id, parent_id)
        self.source_id = source_id or ""
        self.target_id = target_id or ""
        self.style = (
            style
            or "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;"
            "jettySize=auto;loopDirection=0;"
        )

    def to_xml(self):
        connector_cell = ET.Element(
            "mxCell",
            {
                "id": str(self.element_id) if self.element_id else "",
                "value": "",
                "style": self.style,
                "edge": "1",
                "parent": str(self.parent_id) if self.parent_id else "",
                "source": str(self.source_id) if self.source_id else "",
                "target": str(self.target_id) if self.target_id else "",
            },
        )
        geometry = ET.SubElement(
            connector_cell, "mxGeometry", {"relative": "1", "as": "geometry"}
        )
        return connector_cell


class ImageShape(DiagramElement):
    def __init__(self, element_id, parent_id, value, image_url, x, y, width, height):
        super().__init__(element_id, parent_id)
        self.value = value or ""
        self.image_url = image_url or ""
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def to_xml(self):
        image_cell = ET.Element(
            "mxCell",
            {
                "id": str(self.element_id) if self.element_id else "",
                "value": self.value,
                "style": f"shape=image;image={self.image_url};",  # Image style
                "vertex": "1",
                "parent": str(self.parent_id) if self.parent_id else "",
            },
        )
        geometry = ET.SubElement(
            image_cell,
            "mxGeometry",
            {
                "x": str(self.x) if self.x is not None else "0",
                "y": str(self.y) if self.y is not None else "0",
                "width": str(self.width) if self.width is not None else "0",
                "height": str(self.height) if self.height is not None else "0",
                "as": "geometry",
            },
        )
        geometry.set("relative", "0")
        return image_cell


class Annotation(DiagramElement):
    def __init__(self, element_id, parent_id, value, style, x, y, width, height):
        super().__init__(element_id, parent_id)
        self.value = value or ""
        self.style = style or ""
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def to_xml(self):
        annotation_cell = ET.Element(
            "mxCell",
            {
                "id": str(self.element_id) if self.element_id else "",
                "value": self.value,
                "style": self.style,
                "vertex": "1",
                "parent": str(self.parent_id) if self.parent_id else "",
            },
        )
        geometry = ET.SubElement(
            annotation_cell,
            "mxGeometry",
            {
                "x": str(self.x) if self.x is not None else "0",
                "y": str(self.y) if self.y is not None else "0",
                "width": str(self.width) if self.width is not None else "0",
                "height": str(self.height) if self.height is not None else "0",
                "as": "geometry",
            },
        )
        geometry.set("relative", "0")
        return annotation_cell
