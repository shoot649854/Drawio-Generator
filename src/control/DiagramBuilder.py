import base64
import mimetypes
import os

from src.control.XMLGenerator import XMLGenerator
from src.logging.Logging import logger
from src.model.DiagramElement import Annotation, Connector, ImageShape, Shape
from src.model.StyleManager import StyleManager


class DiagramBuilder:
    def __init__(
        self, diagram_id="diagram-id", name="Page-1", output_file="diagram.drawio"
    ):
        self.xml_generator = XMLGenerator()
        self.style_manager = StyleManager()
        self.root = self.xml_generator.add_diagram(
            diagram_id=diagram_id,
            name=name,
            graph_model_attrs={
                "dx": "1422",
                "dy": "794",
                "grid": "1",
                "gridSize": "10",
                "guides": "1",
                "tooltips": "1",
                "connect": "1",
                "arrows": "1",
                "fold": "1",
                "page": "1",
                "pageScale": "1",
                "pageWidth": "850",
                "pageHeight": "1100",
            },
        )
        self.output_file = output_file
        self.current_id = 2

    def add_shape(self, value, shape_type, x, y, width, height, custom_styles=None):
        style = self.style_manager.get_style(shape_type, custom_styles)
        shape = Shape(
            element_id=str(self.current_id),
            parent_id="1",
            value=value,
            style=style,
            x=x,
            y=y,
            width=width,
            height=height,
        )
        self.root.append(shape.to_xml())
        self.current_id += 1
        return shape.element_id

    def add_image_shape(self, value, image_path, x, y, width, height):
        if not os.path.isfile(image_path):
            logger.error(f"Image file not found: {image_path}")
            return None

        # Determine the MIME type based on the file extension
        mime_type, _ = mimetypes.guess_type(image_path)
        if mime_type is None:
            logger.warning(
                f"Could not determine MIME type for {image_path}. Defaulting to image/jpeg."
            )
            mime_type = "image/jpeg"

        with open(image_path, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode("utf-8")

        data_url = f"data:{mime_type};base64,{encoded_string}"
        style = f"shape=image;image={data_url};whiteSpace=wrap;html=1;"

        image_shape = ImageShape(
            element_id=str(self.current_id),
            parent_id="1",
            value=value,
            image_url=data_url,
            x=x,
            y=y,
            width=width,
            height=height,
            # style=style,
        )

        self.root.append(image_shape.to_xml())
        logger.info(f"Added image shape: '{value}' with ID '{image_shape.element_id}'.")
        self.current_id += 1

        return image_shape.element_id

    def add_annotation(self, value, x, y, width, height, custom_styles=None):
        style = custom_styles or "textColor=#000000;align=center;"
        annotation = Annotation(
            element_id=str(self.current_id),
            parent_id="1",
            value=value,
            style=style,
            x=x,
            y=y,
            width=width,
            height=height,
        )
        self.root.append(annotation.to_xml())
        self.current_id += 1
        return annotation.element_id

    def add_connector(self, source_id, target_id, style=None):
        connector = Connector(
            element_id=str(self.current_id),
            parent_id="1",
            source_id=source_id,
            target_id=target_id,
            style=style,
        )
        self.root.append(connector.to_xml())
        self.current_id += 1
        return connector.element_id

    def save(self):
        try:
            self.xml_generator.save_to_file(self.output_file)
            print(f"{self.output_file} has been created successfully.")
        except Exception as e:
            print(f"An error occurred while saving the diagram: {e}")
