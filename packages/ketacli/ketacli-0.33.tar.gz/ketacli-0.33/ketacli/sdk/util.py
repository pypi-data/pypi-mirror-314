from faker import Faker
from jinja2 import Environment, StrictUndefined
from jinja2.exceptions import UndefinedError
from rich.console import Console
import random
import time

faker = Faker()
faker_zh = Faker(locale='zh_CN')


def is_key(key, value_map=None):
    """精确匹配是否存在key

    Args:
        key (str): 字符串key
        value_map (dict, optional): 是否存在该key的字典. Defaults to {}.

    Returns:
        _type_: 最终的key，如果不存在则为None
    """
    if value_map is None:
        value_map = {}
    newkey = key.lower()
    if newkey in value_map:
        return newkey
    return None


def is_fuzzy_key(key, value_map=None):
    """
    检查key或者key的复数形式在map中，并返回最终map中的key
    """
    if value_map is None:
        value_map = {}
    newkey = key.lower()
    if newkey in value_map:
        return newkey
    if newkey.endswith('s'):
        newkey = newkey[:-1]
    else:
        newkey = newkey + 's'
    if newkey in value_map:
        return newkey
    return None


def parse_url_params(url_query):
    params = url_query.lstrip('?')  # 移除开头的问号
    pairs = params.split(',')  # 将参数对分割
    result = {}

    for pair in pairs:
        key, value = pair.split('=')  # 分割键和值
        try:
            value = int(value) if '.' not in value else float(value)  # 尝试转换为整数或浮点数
        except ValueError:
            pass  # 如果转换失败，保留原始字符串值
        result[key] = value  # 添加到结果字典
    return result


class Template:
    def __init__(self, template):
        self.env = Environment(undefined=StrictUndefined)
        self.temp = self.env.from_string(template)
        self.template = template
        all_package = {}
        if isinstance(__builtins__, dict):
            all_package.update(__builtins__)
        else:
            all_package.update(__builtins__.__dict__)
        self.temp.globals.update({"time": time, "faker": faker, "faker_zh": faker_zh, "random": random, **all_package})

    def render(self, **kwargs):
        try:
            return self.temp.render(**kwargs)
        except UndefinedError as e:
            Console().print(
                f"[red]Template rendering failed: {self.template}."
                f" Please provide the [bold yellow]-e/--extra[/bold yellow] argument with required parameters.[/red]"
                f"{e}")
            exit(1)
