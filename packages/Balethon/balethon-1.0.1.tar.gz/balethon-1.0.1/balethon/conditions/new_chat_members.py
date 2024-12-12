from .condition import Condition


@Condition.create
def new_chat_members(event) -> bool:
    from ..objects import Message
    if isinstance(event, Message):
        return bool(event.new_chat_members)
