from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="WebcastLiveAnalyticsUserInteractionsResponseComment")


@_attrs_define
class WebcastLiveAnalyticsUserInteractionsResponseComment:
    """
    Attributes:
        content (str):
        emotes (list[Any]):
        event_time (float):
        msg_id (float):
    """

    content: str
    emotes: list[Any]
    event_time: float
    msg_id: float

    def to_dict(self) -> dict[str, Any]:
        content = self.content

        emotes = self.emotes

        event_time = self.event_time

        msg_id = self.msg_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "content": content,
                "emotes": emotes,
                "event_time": event_time,
                "msg_id": msg_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content = d.pop("content")

        emotes = cast(list[Any], d.pop("emotes"))

        event_time = d.pop("event_time")

        msg_id = d.pop("msg_id")

        webcast_live_analytics_user_interactions_response_comment = cls(
            content=content,
            emotes=emotes,
            event_time=event_time,
            msg_id=msg_id,
        )

        return webcast_live_analytics_user_interactions_response_comment
