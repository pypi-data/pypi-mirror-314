from typing import Literal, List, Union

from pydantic import BaseModel


class Message(BaseModel):
    role: Literal['system', 'user', 'assistant'] = 'user'
    content: str

    def __init__(self, content: str, role: Literal['system', 'user', 'assistant'] = 'user'):
        super().__init__(content=content, role=role)

    def to_dict(self) -> dict:
        return {'role': self.role, 'content': self.content}


class SystemMessage(Message):
    def __init__(self, content: str):
        super().__init__(content, 'system')


class UserMessage(Message):
    def __init__(self, content: str):
        super().__init__(content, 'user')


class AssistantMessage(Message):
    def __init__(self, content: str):
        super().__init__(content, 'assistant')


class MessagesSet(BaseModel):
    message_list: List[Message] = []

    def __init__(self, message_list: List[Message] = None):
        if message_list:
            super().__init__(message_list=message_list)
        else:
            super().__init__()

    def add_user(self, content: str):
        self.message_list.append(UserMessage(content))
        return self

    def add_assistant(self, content: str):
        self.message_list.append(AssistantMessage(content))
        return self

    def add_system(self, content: str):
        if len(self.message_list) == 0:
            self.message_list.append(SystemMessage(content))
        elif not isinstance(self.message_list[-1], SystemMessage):
            self.message_list.append(SystemMessage(content))
        else:
            raise ValueError("MessagesSet exists a system message.")
        return self

    def validate_alternation(self):
        if not self.message_list:
            return False, "MessagesSet为空"

        if self.message_list[0].role not in ("user", "system"):
            return False, "MessagesSet 开始必须为 user or system message."

        if len(self.message_list) >= 2 and self.message_list[0].role == "system" and self.message_list[
            1].role != "user":
            return False, "MessagesSet 开始必须为 user message."

        if self.message_list[-1].role not in ("user", "system"):
            return False, "MessagesSet 结束必须为 user or system message."

        for i in range(len(self.message_list) - 1):
            if self.message_list[i].role == self.message_list[i + 1].role:
                return False, f"MessagesSet 存在 Consecutive messages found at index {i} and {i + 1}."

        return True, "MessagesSet is valid."

    def append_messages(self, messages_set: Union['MessagesSet', List[UserMessage | AssistantMessage]]):
        if type(messages_set) is MessagesSet:
            self.message_list = self.message_list + messages_set.message_list
        else:
            for message in messages_set:
                if type(message) is Message:
                    self.message_list.append(message)
                else:
                    raise ValueError("MessagesSet append_messages type error")
        return self

    def get_messages(self):
        # Validate the message alternation
        is_valid, validation_message = self.validate_alternation()
        if is_valid:
            return [i.to_dict() for i in self.message_list]
        else:
            raise ValueError(validation_message)

    def get_format_messages(self):
        _prompt = [i.to_dict() for i in self.message_list]

        return '\n\n'.join([f'{i["role"]}:\n{i["content"]}' for i in _prompt])

    def get_last_message(self):
        """Returns the last message if available, otherwise returns None."""
        if not self.message_list:
            return None
        return self.message_list[-1]

    def __len__(self):
        return len(self.message_list)

    def __getitem__(self, index):
        return self.message_list[index]

    def __iter__(self):
        for item in self.message_list:
            yield item

    def __repr__(self):
        return f"MessagesSet({self.message_list})"
