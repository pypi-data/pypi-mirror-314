from wbcore.metadata.configs.display.instance_display.shortcuts import (
    Display,
    create_simple_display,
)
from wbcore.metadata.configs.display.instance_display.utils import repeat_field
from wbcore.metadata.configs.preview import PreviewViewConfig


class PortfolioPreviewConfig(PreviewViewConfig):
    def get_display(self) -> Display:
        return create_simple_display(
            [
                [
                    "name",
                    "name",
                    "currency",
                ],
                [repeat_field(2, "portfolio_synchronization"), "last_synchronization"],
                [repeat_field(3, "depends_on")],
            ]
        )
