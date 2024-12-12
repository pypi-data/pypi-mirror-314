from typing import Union, BinaryIO

import balethon
from ...objects import InputMedia, Message


class SendAudio:

    async def send_audio(
            self: "balethon.Client",
            chat_id: Union[int, str],
            audio: Union[str, bytes, BinaryIO, InputMedia],
            caption: str = None,
            duration: int = None,
            title: str = None,
            reply_to_message_id: int = None
    ) -> Message:
        chat_id = await self.resolve_peer_id(chat_id)
        if not isinstance(audio, InputMedia):
            audio = InputMedia(media=audio)
        audio = audio.media
        data = locals()
        del data["self"]
        result = await self.execute("post", "sendAudio", **data)
        result = Message.wrap(result)
        result.bind(self)
        return result
