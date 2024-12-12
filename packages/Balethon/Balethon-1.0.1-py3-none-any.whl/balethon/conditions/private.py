from .condition import Condition


@Condition.create
def private(event) -> bool:
    from ..objects import Message, CallbackQuery
    if isinstance(event, Message):
        event = event.chat.type
    elif isinstance(event, CallbackQuery):
        event = event.message.chat.type
    return event == "private"
