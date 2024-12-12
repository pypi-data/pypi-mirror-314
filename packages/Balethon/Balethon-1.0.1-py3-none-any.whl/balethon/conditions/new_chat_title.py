from .condition import Condition


@Condition.create
def new_chat_title(event) -> bool:
    from ..objects import Message
    if isinstance(event, Message):
        return bool(event.new_chat_title)
