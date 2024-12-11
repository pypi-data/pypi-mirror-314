import json
import re
import xml.etree.ElementTree as ElemTree

ESCAPE_CHAR_MAP = {"\\": "\\\\n",
                   '"': '\\"',
                   "\n": "\\n",
                   "\r": "\\r"}


class Mapper:
    def __init__(self, path):
        self._path: str = path
        self._queries = ElemTree.parse(self._path).getroot()

    def get_query(self, namespace: str, name: str, param: dict | None = None) -> str:
        namespace = self._queries.findall(".//*[@namespace='" + namespace + "']")
        if len(namespace) > 1:
            raise AttributeError("namespace is duplicated")
        if len(namespace) == 0:
            raise AttributeError("namespace is not exist")
        query_strings = namespace[0].findall(".//*[@id='"+name+"']")
        if len(query_strings) > 1:
            raise AttributeError("id of query is duplicated")
        if len(query_strings) == 0:
            raise AttributeError("id of query not exist")
        query = query_strings[0].text
        if param is not None:
            query = parameter_mapping(query, param)
        return query


def parameter_mapping(query: str, param: dict) -> str:
    mapped = re.sub(r"\#\{(.*?)\}", lambda m: mapping(m.group(1), param), query)
    return mapped


def mapping(s: str, param: dict) -> str | None:
    v = param[s]
    if v is None:
        return "NULL"
    elif type(v) == int or type(param[s]) == float:
        return str(v)
    elif type(v) == dict:
        v = dict_replace_value(v)
        v = str(json.dumps(v, ensure_ascii=False))
        return "'" + v + "'"
    elif type(v) == str:
        v = v.replace("'", '"')
        return "'" + v + "'"


def dict_replace_value(d: dict) -> dict:
    x = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = dict_replace_value(v)
        elif isinstance(v, list):
            v = list_replace_value(v)
        elif isinstance(v, str):
            v = v.replace("'", '"')
            for old, new in ESCAPE_CHAR_MAP.items():
                v = v.replace(old, new)
        else:
            v = str(v)
        x[k] = v
    return x


def list_replace_value(l: list) -> list:
    x = []
    for e in l:
        if isinstance(e, list):
            e = list_replace_value(e)
        elif isinstance(e, dict):
            e = dict_replace_value(e)
        elif isinstance(e, str):
            for old, new in ESCAPE_CHAR_MAP.items():
                e = e.replace(old, new)
        x.append(e)
    return x
