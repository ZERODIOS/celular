from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="WebcastRoomChatPayloadV1")


@_attrs_define
class WebcastRoomChatPayloadV1:
    """
    Attributes:
        content (str): The chat message content to send
        target_room_id (str | Unset): The room ID to send the chat to (either this or targetUniqueId is required)
        target_unique_id (str | Unset): The username of the room to send the chat to (either this or targetRoomId is
            required)
        session_id (str | Unset):
        tt_target_idc (str | Unset):
        room_id (str | Unset):
    """

    content: str
    target_room_id: str | Unset = UNSET
    target_unique_id: str | Unset = UNSET
    session_id: str | Unset = UNSET
    tt_target_idc: str | Unset = UNSET
    room_id: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        content = self.content

        target_room_id = self.target_room_id

        target_unique_id = self.target_unique_id

        session_id = self.session_id

        tt_target_idc = self.tt_target_idc

        room_id = self.room_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "content": content,
            }
        )
        if target_room_id is not UNSET:
            field_dict["targetRoomId"] = target_room_id
        if target_unique_id is not UNSET:
            field_dict["targetUniqueId"] = target_unique_id
        if session_id is not UNSET:
            field_dict["sessionId"] = session_id
        if tt_target_idc is not UNSET:
            field_dict["ttTargetIdc"] = tt_target_idc
        if room_id is not UNSET:
            field_dict["roomId"] = room_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content = d.pop("content")

        target_room_id = d.pop("targetRoomId", UNSET)

        target_unique_id = d.pop("targetUniqueId", UNSET)

        session_id = d.pop("sessionId", UNSET)

        tt_target_idc = d.pop("ttTargetIdc", UNSET)

        room_id = d.pop("roomId", UNSET)

        webcast_room_chat_payload_v1 = cls(
            content=content,
            target_room_id=target_room_id,
            target_unique_id=target_unique_id,
            session_id=session_id,
            tt_target_idc=tt_target_idc,
            room_id=room_id,
        )

        return webcast_room_chat_payload_v1
