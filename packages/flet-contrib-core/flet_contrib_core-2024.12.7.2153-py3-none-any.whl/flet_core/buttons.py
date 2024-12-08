from dataclasses import dataclass, field
from typing import Dict, Optional, Union

from flet_core.alignment import Alignment
from flet_core.border import BorderSide
from flet_core.text_style import TextStyle
from flet_core.types import (
    BorderRadiusValue,
    ControlState,
    PaddingValue,
    Number,
    ThemeVisualDensity,
    VisualDensity,
    MouseCursor,
)


@dataclass
class OutlinedBorder:
    pass


@dataclass
class StadiumBorder(OutlinedBorder):
    def __post_init__(self):
        self.type = "stadium"


@dataclass
class RoundedRectangleBorder(OutlinedBorder):
    radius: BorderRadiusValue = field(default=None)

    def __post_init__(self):
        self.type = "roundedRectangle"


@dataclass
class CircleBorder(OutlinedBorder):
    type: str = field(default="circle")


@dataclass
class BeveledRectangleBorder(OutlinedBorder):
    radius: BorderRadiusValue = field(default=None)

    def __post_init__(self):
        self.type = "beveledRectangle"


@dataclass
class ContinuousRectangleBorder(OutlinedBorder):
    radius: BorderRadiusValue = field(default=None)

    def __post_init__(self):
        self.type = "continuousRectangle"


@dataclass
class ButtonStyle:
    color: Union[None, str, Dict[Union[str, ControlState], str]] = field(default=None)
    bgcolor: Union[None, str, Dict[Union[str, ControlState], str]] = field(default=None)
    overlay_color: Union[None, str, Dict[Union[str, ControlState], str]] = field(
        default=None
    )
    shadow_color: Union[None, str, Dict[Union[str, ControlState], str]] = field(
        default=None
    )
    surface_tint_color: Union[None, str, Dict[Union[str, ControlState], str]] = field(
        default=None
    )
    elevation: Union[
        None, float, int, Dict[Union[str, ControlState], Union[float, int]]
    ] = field(default=None)
    animation_duration: Optional[int] = field(default=None)
    padding: Union[PaddingValue, Dict[Union[str, ControlState], PaddingValue]] = field(
        default=None
    )
    side: Union[None, BorderSide, Dict[Union[str, ControlState], BorderSide]] = field(
        default=None
    )
    shape: Union[
        None, OutlinedBorder, Dict[Union[str, ControlState], OutlinedBorder]
    ] = field(default=None)
    alignment: Union[
        None, Alignment, Dict[Union[str, ControlState], Alignment]
    ] = field(default=None)
    enable_feedback: Union[None, bool, Dict[Union[str, ControlState], bool]] = field(
        default=None
    )
    text_style: Union[
        None, TextStyle, Dict[Union[str, ControlState], TextStyle]
    ] = field(default=None)
    icon_size: Union[None, Number, Dict[Union[str, ControlState], Number]] = field(
        default=None
    )
    icon_color: Union[None, str, Dict[Union[str, ControlState], str]] = field(
        default=None
    )
    visual_density: Union[
        None,
        Union[VisualDensity, ThemeVisualDensity],
        Dict[Union[str, ControlState], Union[VisualDensity, ThemeVisualDensity]],
    ] = field(default=None)
    mouse_cursor: Union[
        None, MouseCursor, Dict[Union[str, ControlState], MouseCursor]
    ] = field(default=None)
