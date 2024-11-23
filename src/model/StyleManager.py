class StyleManager:
    def __init__(self):
        self.styles = {
            "rectangle": "rounded=0;whiteSpace=wrap;html=1;",
            "ellipse": "ellipse;whiteSpace=wrap;html=1;",
            # Add more default styles as needed
        }

    def get_style(self, shape_type, custom_styles=None):
        style = self.styles.get(shape_type, "whiteSpace=wrap;html=1;")
        if custom_styles:
            style += custom_styles
        return style

    def add_style(self, shape_type, style_string):
        self.styles[shape_type] = style_string
