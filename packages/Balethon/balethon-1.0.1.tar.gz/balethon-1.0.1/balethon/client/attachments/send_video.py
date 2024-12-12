from typing import Union, BinaryIO

import balethon
from ...objects import InputMedia, Message


class SendVideo:

    async def send_video(
            self: "balethon.Client",
            chat_id: Union[int, str],
            video: Union[str, bytes, BinaryIO, InputMedia],
            duration: int = None,
            width: int = None,
            height: int = None,
            caption: str = None,
            reply_to_message_id: int = None
    ) -> Message:
        chat_id = await self.resolve_peer_id(chat_id)
        if not isinstance(video, InputMedia):
            video = InputMedia(media=video)
        video = video.media
        data = locals()
        del data["self"]
        result = await self.execute("post", "sendVideo", **data)
        result = Message.wrap(result)
        result.bind(self)
        return result
