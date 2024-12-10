# Generated code. Do not modify.
# flake8: noqa: F401, F405, F811

from __future__ import annotations

import enum
import typing

from pydivkit.core import BaseDiv, Expr, Field

from . import div_fixed_size


# A mask to hide text (spoiler) that looks like randomly distributed particles
# (telegram alike).
class DivTextRangeMaskParticles(BaseDiv):

    def __init__(
        self, *,
        type: str = "particles",
        color: typing.Optional[typing.Union[Expr, str]] = None,
        density: typing.Optional[typing.Union[Expr, float]] = None,
        is_animated: typing.Optional[typing.Union[Expr, bool]] = None,
        is_enabled: typing.Optional[typing.Union[Expr, bool]] = None,
        particle_size: typing.Optional[div_fixed_size.DivFixedSize] = None,
        **kwargs: typing.Any,
    ):
        super().__init__(
            type=type,
            color=color,
            density=density,
            is_animated=is_animated,
            is_enabled=is_enabled,
            particle_size=particle_size,
            **kwargs,
        )

    type: str = Field(default="particles")
    color: typing.Union[Expr, str] = Field(
        format="color", 
        description="Color of particles on the mask.",
    )
    density: typing.Optional[typing.Union[Expr, float]] = Field(
        description=(
            "Density of particles on the mask, interpreted as a "
            "probability of a particle tospawn in a given point on the "
            "mask."
        ),
    )
    is_animated: typing.Optional[typing.Union[Expr, bool]] = Field(
        description=(
            "Defines whether particles on the mask will be animated or "
            "not. Animation lookslike smooth random particle movements "
            "(telegram alike)."
        ),
    )
    is_enabled: typing.Optional[typing.Union[Expr, bool]] = Field(
        description=(
            "Controls mask state: if set to `true` mask will hide "
            "specified part of the text,otherwise the text will be "
            "shown."
        ),
    )
    particle_size: typing.Optional[div_fixed_size.DivFixedSize] = Field(
        description="Size of a single particle on a mask.",
    )


DivTextRangeMaskParticles.update_forward_refs()
