import time
from typing import Any, Optional, Union

from flet_core.adaptive_control import AdaptiveControl
from flet_core.buttons import ButtonStyle
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    ClipBehavior,
    UrlTarget,
    OptionalEventCallable,
)
from flet_core.utils import deprecated


class ElevatedButton(ConstrainedControl, AdaptiveControl):
    """
    Elevated buttons are essentially filled tonal buttons with a shadow. To prevent shadow creep, only use them when absolutely necessary, such as when the button requires visual separation from a patterned background.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "Basic elevated buttons"
        page.add(
            ft.ElevatedButton(text="Elevated button"),
            ft.ElevatedButton("Disabled button", disabled=True),
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/elevatedbutton
    """

    def __init__(
        self,
        text: Optional[str] = None,
        icon: Optional[str] = None,
        icon_color: Optional[str] = None,
        color: Optional[str] = None,
        bgcolor: Optional[str] = None,
        content: Optional[Control] = None,
        elevation: OptionalNumber = None,
        style: Optional[ButtonStyle] = None,
        autofocus: Optional[bool] = None,
        clip_behavior: Optional[ClipBehavior] = None,
        url: Optional[str] = None,
        url_target: Optional[UrlTarget] = None,
        on_click: OptionalEventCallable = None,
        on_long_press: OptionalEventCallable = None,
        on_hover: OptionalEventCallable = None,
        on_focus: OptionalEventCallable = None,
        on_blur: OptionalEventCallable = None,
        #
        # ConstrainedControl and AdaptiveControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        on_animation_end: OptionalEventCallable = None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        adaptive: Optional[bool] = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.__color = None
        self.__bgcolor = None
        self.__elevation = None

        self.text = text
        self.color = color
        self.bgcolor = bgcolor
        self.elevation = elevation
        self.style = style
        self.icon = icon
        self.icon_color = icon_color
        self.content = content
        self.autofocus = autofocus
        self.url = url
        self.url_target = url_target
        self.on_click = on_click
        self.on_long_press = on_long_press
        self.on_hover = on_hover
        self.on_focus = on_focus
        self.on_blur = on_blur
        self.clip_behavior = clip_behavior

    def _get_control_name(self):
        return "elevatedbutton"

    def before_update(self):
        super().before_update()
        assert (
            self.text or self.icon or (self.__content and self.__content.visible)
        ), "at minimum, text, icon or a visible content must be provided"
        if any([self.__color, self.__bgcolor, self.__elevation]):
            self.__style = self.__style or ButtonStyle()
        if self.__style:
            self.__style.color = (
                self.__style.color if self.__style.color is not None else self.color
            )
            self.__style.bgcolor = (
                self.__style.bgcolor
                if self.__style.bgcolor is not None
                else self.bgcolor
            )
            self.__style.elevation = (
                self.__style.elevation
                if self.__style.elevation is not None
                else self.elevation
            )
            self.__style.side = self._wrap_attr_dict(self.__style.side)
            self.__style.shape = self._wrap_attr_dict(self.__style.shape)
            self.__style.padding = self._wrap_attr_dict(self.__style.padding)
            self.__style.text_style = self._wrap_attr_dict(self.__style.text_style)
        self._set_attr_json("style", self.__style)

    def _get_children(self):
        if self.__content is None:
            return []
        self.__content._set_attr_internal("n", "content")
        return [self.__content]

    def focus(self):
        self._set_attr_json("focus", str(time.time()))
        self.update()

    @deprecated(
        reason="Use focus() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def focus_async(self):
        self.focus()

    # text
    @property
    def text(self) -> Optional[str]:
        return self._get_attr("text")

    @text.setter
    def text(self, value: Optional[str]):
        self._set_attr("text", value)

    # color
    @property
    def color(self) -> Optional[str]:
        return self.__color

    @color.setter
    def color(self, value: Optional[str]):
        self.__color = value

    # bgcolor
    @property
    def bgcolor(self) -> Optional[str]:
        return self.__bgcolor

    @bgcolor.setter
    def bgcolor(self, value: Optional[str]):
        self.__bgcolor = value
        self._set_attr("bgColor", value)

    # elevation
    @property
    def elevation(self) -> OptionalNumber:
        return self.__elevation

    @elevation.setter
    def elevation(self, value: OptionalNumber):
        self.__elevation = value

    # style
    @property
    def style(self) -> Optional[ButtonStyle]:
        return self.__style

    @style.setter
    def style(self, value: Optional[ButtonStyle]):
        self.__style = value

    # icon
    @property
    def icon(self) -> Optional[str]:
        return self._get_attr("icon")

    @icon.setter
    def icon(self, value: Optional[str]):
        self._set_attr("icon", value)

    # icon_color
    @property
    def icon_color(self) -> Optional[str]:
        return self._get_attr("iconColor")

    @icon_color.setter
    def icon_color(self, value: Optional[str]):
        self._set_attr("iconColor", value)

    # url
    @property
    def url(self) -> Optional[str]:
        return self._get_attr("url")

    @url.setter
    def url(self, value: Optional[str]):
        self._set_attr("url", value)

    # url_target
    @property
    def url_target(self) -> Optional[UrlTarget]:
        return self.__url_target

    @url_target.setter
    def url_target(self, value: Optional[UrlTarget]):
        self.__url_target = value
        self._set_enum_attr("urlTarget", value, UrlTarget)

    # on_click
    @property
    def on_click(self):
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler):
        self._add_event_handler("click", handler)

    # on_long_press
    @property
    def on_long_press(self):
        return self._get_event_handler("long_press")

    @on_long_press.setter
    def on_long_press(self, handler):
        self._add_event_handler("long_press", handler)
        self._set_attr("onLongPress", True if handler is not None else None)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # autofocus
    @property
    def autofocus(self) -> Optional[bool]:
        return self._get_attr("autofocus", data_type="bool", def_value=False)

    @autofocus.setter
    def autofocus(self, value: Optional[bool]):
        self._set_attr("autofocus", value)

    # clip_behavior
    @property
    def clip_behavior(self) -> Optional[ClipBehavior]:
        return self.__clip_behavior

    @clip_behavior.setter
    def clip_behavior(self, value: Optional[ClipBehavior]):
        self.__clip_behavior = value
        self._set_enum_attr("clipBehavior", value, ClipBehavior)

    # on_hover
    @property
    def on_hover(self) -> OptionalEventCallable:
        return self._get_event_handler("hover")

    @on_hover.setter
    def on_hover(self, handler: OptionalEventCallable):
        self._add_event_handler("hover", handler)
        self._set_attr("onHover", True if handler is not None else None)

    # on_focus
    @property
    def on_focus(self) -> OptionalEventCallable:
        return self._get_event_handler("focus")

    @on_focus.setter
    def on_focus(self, handler: OptionalEventCallable):
        self._add_event_handler("focus", handler)

    # on_blur
    @property
    def on_blur(self) -> OptionalEventCallable:
        return self._get_event_handler("blur")

    @on_blur.setter
    def on_blur(self, handler: OptionalEventCallable):
        self._add_event_handler("blur", handler)
