# Generated code. Do not modify.
# flake8: noqa: F401, F405, F811

from __future__ import annotations

import enum
import typing

from pydivkit.core import BaseDiv, Expr, Field


# The page size is equal to the size of its content.
class DivPageContentSize(BaseDiv):

    def __init__(
        self, *,
        type: str = "wrap_content",
        alignment: typing.Optional[typing.Union[Expr, DivPageContentSizeAlignment]] = None,
        **kwargs: typing.Any,
    ):
        super().__init__(
            type=type,
            alignment=alignment,
            **kwargs,
        )

    type: str = Field(default="wrap_content")
    alignment: typing.Optional[typing.Union[Expr, DivPageContentSizeAlignment]] = Field(
        description=(
            "Alignment of pager pages along the scroll axis. For edge "
            "alignment, the marginfrom the edge of the parent equals the "
            "value of the corresponding padding."
        ),
    )


class DivPageContentSizeAlignment(str, enum.Enum):
    START = "start"
    CENTER = "center"
    END = "end"


DivPageContentSize.update_forward_refs()
