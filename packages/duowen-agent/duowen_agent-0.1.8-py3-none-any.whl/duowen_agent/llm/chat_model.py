import logging
import os
from typing import List

from duowen_agent.error import LLMError, LengthLimitExceededError, MaxTokenExceededError
from duowen_agent.llm.entity import UserMessage, AssistantMessage, SystemMessage, MessagesSet
from openai import OpenAI


class OpenAIChat:
    def __init__(self, base_url: str = None, model: str = 'gpt-3.5-turbo', api_key: str = None, temperature=0.2,
                 timeout=120, token_limit=4 * 1024, extra_headers=None, **kwargs):
        self.base_url = base_url if base_url else os.environ.get("OPENAI_BASE_URL")
        self.api_key = api_key if api_key else os.environ.get("OPENAI_API_KEY", "xxx")
        self.temperature = temperature
        self.model = model
        self.timeout = timeout
        self.token_limit = token_limit
        self.extra_headers = extra_headers
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url, timeout=self.timeout)

    @staticmethod
    def _check_message(message: str | List[dict] | MessagesSet) -> List[dict]:
        if isinstance(message, str):
            return [SystemMessage("You are a helpful assistant").to_dict(), UserMessage(message).to_dict()]
        elif type(message) is MessagesSet:
            return message.get_messages()
        elif isinstance(message, List) and all(isinstance(i, dict) for i in message):
            return message
        else:
            raise ValueError(f"message 格式非法:{str(message)}")

    def _build_params(self, messages: str | List[dict], temperature: float = None, max_new_tokens: int = None,
                      top_p=None, timeout=30):
        _params = {'messages': self._check_message(messages), 'model': self.model}

        if temperature:
            _params['temperature'] = temperature
        elif self.temperature:
            _params['temperature'] = self.temperature
        else:
            _params['temperature'] = 0.4

        if max_new_tokens:
            _params['max_tokens'] = max_new_tokens
        else:
            _params['max_tokens'] = 2000

        if top_p:
            _params['top_p'] = top_p
            # 如果用户调整 top_p 则删除 temperature 设置
            del _params['temperature']

        if timeout:
            _params['timeout'] = timeout
        elif self.timeout:
            _params['timeout'] = self.timeout

        if self.extra_headers:
            _params['extra_headers'] = self.extra_headers

        return _params

    def _chat_stream(self, messages, temperature: float = None, max_new_tokens: int = None, top_p=None, timeout=30):

        _params = self._build_params(messages, temperature, max_new_tokens, top_p, timeout)
        _params['stream'] = True

        try:

            response = self.client.chat.completions.create(**_params)

            _full_message = ""
            for chunk in response:
                if chunk.choices:
                    if chunk.choices[0].finish_reason == 'length':
                        raise LengthLimitExceededError(content=_full_message)
                    elif chunk.choices[0].finish_reason == 'max_tokens':
                        raise MaxTokenExceededError(content=_full_message)

                    _msg = chunk.choices[0].delta.content or ""
                    _full_message += _msg
                    if _msg:
                        yield _msg

            if not _full_message:  # 如果流式输出返回为空
                raise LLMError("语言模型流式输出无响应", self.base_url, self.model, messages)

        except (LengthLimitExceededError, MaxTokenExceededError) as e:
            raise e

        except Exception as e:
            raise LLMError(str(e), self.base_url, self.model, messages)

    def _chat(self, messages, temperature: float = None, max_new_tokens: int = None, top_p=None, timeout=30):

        _params = self._build_params(messages, temperature, max_new_tokens, top_p, timeout)
        _params['stream'] = False

        try:
            response = self.client.chat.completions.create(**_params)

            if response.choices[0].finish_reason == "length":
                raise LengthLimitExceededError(content=response.choices[0].message.content)
            elif response.choices[0].finish_reason == 'max_tokens':
                raise MaxTokenExceededError(content=response.choices[0].message.content)
            else:
                _msg = response.choices[0].message.content
                if _msg:
                    return _msg
                else:
                    raise LLMError("语言模型无消息回复", self.base_url, self.model, messages)
        except (LengthLimitExceededError, MaxTokenExceededError) as e:
            raise e

        except Exception as e:
            raise LLMError(str(e), self.base_url, self.model, messages)

    def chat_for_stream(self, messages, temperature: float = None, max_tokens: int = None, top_p=None, timeout=30,
                        continue_cnt: int = 0):

        if continue_cnt == 0:
            yield from self._chat_stream(messages, temperature, max_tokens, top_p, timeout)

        _response_finished = False
        _full_message = ""
        _ori_messages = self._check_message(messages)
        _continue_cnt = continue_cnt

        while 1:
            if _response_finished is True:
                break

            if _continue_cnt < 0:
                logging.warning(f"续写模式达到 {continue_cnt if continue_cnt else 2} 次上限, 退出.")
                break

            try:

                if _full_message:
                    logging.info("触发LLM模型chat续写模式")
                    _messages = _ori_messages + [AssistantMessage(_full_message).to_dict()] + [
                        UserMessage("continue").to_dict()]
                else:
                    _messages = _ori_messages

                for i in self._chat_stream(_messages, temperature, max_tokens, top_p, timeout):
                    _full_message += i
                    yield i
                _response_finished = True
            except LengthLimitExceededError as e:
                pass

    def chat(self, messages: str | List[dict] | MessagesSet, temperature: float = None, max_tokens: int = None,
             top_p=None, timeout=30, continue_cnt: int = 0):

        if continue_cnt == 0:
            return self._chat(messages, temperature, max_tokens, top_p, timeout)

        _response_finished = False
        _full_message = ""
        _ori_messages = self._check_message(messages)
        _continue_cnt = continue_cnt

        while 1:
            if _response_finished is True:
                break

            if _continue_cnt < 0:
                logging.warning(f"续写模式达到 {continue_cnt if continue_cnt else 2} 次上限, 退出.")
                break

            try:
                if _full_message:
                    logging.info("触发LLM模型chat续写模式")
                    _messages = _ori_messages + [AssistantMessage(_full_message).to_dict()] + [
                        UserMessage("continue").to_dict()]
                else:
                    _messages = _ori_messages
                _response_msg = self._chat(_messages, temperature, max_tokens, top_p, timeout)
                _full_message += _response_msg
                _response_finished = True
            except LengthLimitExceededError as e:
                _full_message += e.content
            finally:
                _continue_cnt -= 1
        return _full_message
