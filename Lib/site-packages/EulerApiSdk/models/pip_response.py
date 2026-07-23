from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PipResponse")


@_attrs_define
class PipResponse:
    """
    Attributes:
        code (float):
        image_url (str):
        label (str):
        value (float):
        unit (str):
        message (str | Unset):
    """

    code: float
    image_url: str
    label: str
    value: float
    unit: str
    message: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        image_url = self.image_url

        label = self.label

        value = self.value

        unit = self.unit

        message = self.message

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "code": code,
                "image_url": image_url,
                "label": label,
                "value": value,
                "unit": unit,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = d.pop("code")

        image_url = d.pop("image_url")

        label = d.pop("label")

        value = d.pop("value")

        unit = d.pop("unit")

        message = d.pop("message", UNSET)

        pip_response = cls(
            code=code,
            image_url=image_url,
            label=label,
            value=value,
            unit=unit,
            message=message,
        )

        return pip_response
