import json
import os
import sys
from typing import Any, Dict, List

from src.config import DATA_PATH
from src.control.DiagramBuilder import DiagramBuilder
from src.logging.Logging import logger


def load_json_data(file_path: str) -> Dict[str, Any]:
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            logger.info(f"Successfully loaded JSON data from '{file_path}'.")
            return data
    except FileNotFoundError:
        logger.error(f"JSON file not found: '{file_path}'.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from '{file_path}': {e}")
        sys.exit(1)


def map_shapes_to_ids(shapes: List[Dict], builder: "DiagramBuilder") -> Dict[str, str]:
    value_to_id = {}
    for shape in shapes:
        shape_type = shape.get("type", "rectangle")
        value = shape.get("value", "")
        x = shape.get("x", 0)
        y = shape.get("y", 0)
        width = shape.get("width", 80)
        height = shape.get("height", 40)
        styles = shape.get("styles", "")

        if shape_type == "image":
            image_url = shape.get("image_url", "")
            # Ensure the image path is relative
            image_path = os.path.normpath(image_url)
            shape_id = builder.add_image_shape(
                value=value, image_path=image_path, x=x, y=y, width=width, height=height
            )
            logger.info(f"Added image shape: '{value}' with ID '{shape_id}'.")
        else:
            shape_id = builder.add_shape(
                value=value,
                shape_type=shape_type,
                x=x,
                y=y,
                width=width,
                height=height,
                custom_styles=styles,
            )
            logger.info(
                f"Added shape: '{value}' of type '{shape_type}' with ID '{shape_id}'."
            )

        if value:
            value_to_id[value] = shape_id
        else:
            logger.warning(f"Shape without a 'value' field encountered: {shape}.")

    return value_to_id


def add_connectors(
    connectors: list, value_to_id: Dict[str, str], builder: DiagramBuilder
) -> None:
    for connector in connectors:
        source_value = connector.get("source", "")
        target_value = connector.get("target", "")
        style = connector.get("style", "")

        source_id = value_to_id.get(source_value)
        target_id = value_to_id.get(target_value)

        if source_id and target_id:
            builder.add_connector(source_id=source_id, target_id=target_id, style=style)
            logger.info(f"Added connector from '{source_value}' to '{target_value}'.")
        else:
            logger.warning(
                f"Connector from '{source_value}' to '{target_value}' cannot be created. "
                f"Source ID: '{source_id}', Target ID: '{target_id}'."
            )


def add_annotations(annotations: list, builder: DiagramBuilder) -> None:
    for annotation in annotations:
        value = annotation.get("value", "")
        x = annotation.get("x", 0)
        y = annotation.get("y", 0)
        width = annotation.get("width", 200)
        height = annotation.get("height", 40)
        styles = annotation.get("styles", "")

        builder.add_annotation(
            value=value, x=x, y=y, width=width, height=height, custom_styles=styles
        )
        logger.info(f"Added annotation: '{value}'.")


def main() -> None:
    builder = DiagramBuilder(output_file="architecture_diagram.json_based.drawio")
    data = load_json_data(DATA_PATH)

    shapes = data.get("shapes", [])
    value_to_id = map_shapes_to_ids(shapes, builder)

    connectors = data.get("connectors", [])
    add_connectors(connectors, value_to_id, builder)

    annotations = data.get("annotations", [])
    add_annotations(annotations, builder)

    try:
        builder.save()
        logger.info(
            "architecture_diagram.json_based.drawio has been created successfully."
        )
    except Exception as e:
        logger.error(f"An error occurred while saving the diagram: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
