import logging
import random
import string
import time
from functools import wraps
from importlib import import_module
from typing import Callable, Dict, List, Optional, Type

import json5
from pydantic import ValidationError, BaseModel

from duowen_agent.error import ObserverException

logger = logging.getLogger(__name__)


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.

    Args:
        dotted_path: eg promptulate.schema.MessageSet

    Returns:
        Class corresponding to dotted path.
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (module_path, class_name)) from err


def listdict_to_string(data: List[Dict], prefix: Optional[str] = "", suffix: Optional[str] = "\n",
                       item_prefix: Optional[str] = "", item_suffix: Optional[str] = ";\n\n",
                       is_wrap: bool = True, ) -> str:
    """Convert List[Dict] type data to string type"""
    wrap_ch = "\n" if is_wrap else ""
    result = f"{prefix}"
    for item in data:
        temp_list = ["{}:{} {}".format(k, v, wrap_ch) for k, v in item.items()]
        result += f"{item_prefix}".join(temp_list) + f"{item_suffix}"
    result += suffix
    return result[:-2]


def generate_unique_id() -> str:
    timestamp = int(time.time() * 1000)
    random_string = "".join(random.choices(string.ascii_letters + string.digits, k=6))

    unique_id = f"dw-{timestamp}-{random_string}"
    return unique_id


def convert_backslashes(path: str):
    """Convert all \\ to / of file path."""
    return path.replace("\\", "/")


def hint(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        ret = fn(*args, **kwargs)
        logger.debug(f"function {fn.__name__} is running now")
        return ret

    return wrapper


def record_time():
    def decorator(fn: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Callable:
            start_time = time.time()
            ret = fn(*args, **kwargs)
            duration = time.time() - start_time
            logger.debug(f"[duowen-agent timer] <{fn.__name__}> run {duration}s")
            return ret

        return wrapper

    return decorator


def retrying(_func, _max_retries=3, **kwargs):
    for attempt in range(_max_retries):
        try:
            return _func(**kwargs)
        except ObserverException:
            if attempt == _max_retries - 1:
                raise
            else:
                time.sleep(0.1)
                continue
        except Exception as e:
            raise


def parse_json_markdown(json_string: str) -> dict:
    # Get json from the backticks/braces
    json_string = json_string.strip()
    starts = ["```json", "```", "``", "`", "{"]
    ends = ["```", "``", "`", "}"]
    end_index = -1
    for s in starts:
        start_index = json_string.find(s)
        if start_index != -1:
            if json_string[start_index] != "{":
                start_index += len(s)
            break
    if start_index != -1:
        for e in ends:
            end_index = json_string.rfind(e, start_index)
            if end_index != -1:
                if json_string[end_index] == "}":
                    end_index += 1
                break
    if start_index != -1 and end_index != -1 and start_index < end_index:
        extracted_content = json_string[start_index:end_index].strip()
        logging.info(f"parse_json_markdown content: {extracted_content} {start_index} {end_index}")
        parsed = json5.loads(extracted_content)
    else:
        raise Exception("Could not find JSON block in the output.")

    return parsed


def json_observation(content: str, pydantic_obj: Type[BaseModel]):
    try:
        _data1 = parse_json_markdown(content)
    except ValueError as e:
        raise ObserverException(predict_value=content, expect_value="json格式数据",
                                err_msg=f"observation error jsonload, msg: {str(e)}")
    try:
        return pydantic_obj(**_data1)
    except ValidationError as e:
        raise ObserverException(predict_value=content, expect_value=str(pydantic_obj.model_json_schema()),
                                err_msg=f"observation error ValidationError, msg: {str(e)}")
