import asyncio
import copy
import inspect
import json
import os
import re
from collections import OrderedDict
import datetime

from .ArrayHelper import ArrayHelper
from .ExtException import ExtException, HandlerNotFoundError


class Helper:

    @staticmethod
    def get_obj_class(path, obj_name, *, folder=False, suffix=None):
        folder_name = f'.{obj_name}' if folder else ''
        class_name = obj_name
        if suffix:
            class_name += suffix
        full_path = f'{path}{folder_name}.{class_name}.{class_name}'
        try:
            return Helper.get_class(full_path)
        except ExtException as err:
            raise HandlerNotFoundError(detail=f'object {obj_name}', parent=err)

    @staticmethod
    def get_class(class_full_path):
        try:
            parts = class_full_path.split('.')
            module = ".".join(parts[:-1])
            m = __import__(module)
            for comp in parts[1:]:
                m = getattr(m, comp)
            return m
        except ImportError as e:
            # ошибки в классе или нет файла
            raise ImportError(f'get_class({class_full_path}: {str(e)}')
        except AttributeError as e:
            # Нет такого класса
            raise AttributeError(f'get_class({class_full_path}: {str(e)}')
        except Exception as e:
            # ошибки в классе
            raise Exception(f'get_class({class_full_path}: {str(e)}')

    @classmethod
    def loads_exception(cls, data):
        try:
            data = json.loads(data)
            _handler = Helper.get_class(f'{data["__module__"]}.{data["__name__"]}')
            return _handler(**data)
        except Exception as err:
            return ExtException(dump=data, action='Helper.loads_exception', parent=err)

    @staticmethod
    def update_dict(*args):
        size = len(args)
        if size == 1:
            return Helper._update_dict({}, args[0])
        elif size > 1:
            result = args[0]
            for i in range(size - 1):
                result = Helper._update_dict(result, args[i + 1])
            return result

    @staticmethod
    def _update_dict(base, new, _path=''):
        if not new:
            return base
        for element in new:
            try:
                if element in base and base[element] is not None:
                    if isinstance(new[element], dict):
                        if isinstance(base[element], dict):
                            base[element] = Helper._update_dict(base[element], new[element], f'{_path}.{element}')
                        else:
                            raise ExtException(
                                message='type mismatch',
                                detail=f'{type(base[element])} in {_path}.{element}',
                                dump={'value': str(base[element])}
                            )
                    elif isinstance(new[element], list):
                        base[element] = ArrayHelper.unique_extend(base[element], new[element])
                    else:
                        base[element] = new[element]
                else:
                    try:
                        base[element] = copy.deepcopy(new[element])
                    except TypeError as e:
                        if not base:
                            base = {
                                element: copy.deepcopy(new[element])
                            }
                        else:
                            raise NotImplementedError()
            except ExtException as err:
                raise ExtException(parent=err) from err
            except Exception as err:
                raise ExtException(
                    parent=err,
                    action='Helper.update_dict',
                    detail='{0}({1})'.format(err, _path),
                    dump={
                        'element': element,
                        'message': str(err)
                    })
        return base

    @classmethod
    def xml_to_json(cls, elem, array_mode):
        if not array_mode:
            d = OrderedDict()
            for key, value in elem.attrib.items():
                # d.__setitem__(d, "key", value)
                d[key] = value
            elem_text = elem.text
            if elem_text is None:
                d = elem.tag
            else:
                elem_text = elem_text.strip()
                if elem_text:
                    # d.__setitem__(d, "Значение", elem_text)
                    d["Значение"] = elem_text
        else:
            d = []
        array = OrderedDict()
        item_name = ''
        names_check = {"main": [], "sub": {}}
        for sub_elem in elem:
            this_array = True if sub_elem.find("[@Имя]") else False
            try:
                value = cls.xml_to_json(sub_elem, this_array)
            except Exception as error:
                element = sub_elem.tag + (
                    "." + sub_elem.get('Имя') if this_array else "") + "." + error.detail if hasattr(
                    error, 'detail') else ''
                raise ExtException(parent=error, dump={'element': element})
            if this_array:
                item_name = sub_elem.get('Имя')
                if array_mode:
                    # Проверяем повторение подэлементов при наличии узла Имя, так как все одноименные узлы
                    # с таким атрибутом будут слиты в 1, а по атрибуту "Имя" добавлены как элементы.
                    # Одинаковых атрибутов "Имя" в рамках одноименных узлов быть не должно
                    sub_checked = []
                    if sub_elem.tag in names_check["sub"]:
                        sub_checked = names_check["sub"][sub_elem.tag]
                    if item_name in sub_checked:
                        raise ExtException(message='Дублирующиеся узлы в xml файле.',
                                           dump=sub_elem.tag + "." + item_name)
                    sub_checked.append(item_name)
                    names_check["sub"][sub_elem.tag] = sub_checked
                    if sub_elem.tag not in array:
                        if sub_elem.tag == item_name:
                            array[sub_elem.tag] = value
                        else:
                            array[sub_elem.tag] = OrderedDict()
                        d.append({"Имя": sub_elem.tag, "Значение": array[sub_elem.tag]})
                    if sub_elem.tag != item_name:
                        array[sub_elem.tag][item_name] = value
                else:
                    if sub_elem.tag not in d:
                        d[sub_elem.tag] = OrderedDict()
                    if sub_elem.tag == item_name:
                        d[sub_elem.tag] = value
                    else:
                        d[sub_elem.tag][item_name] = value
            else:
                if array_mode:
                    # Тут просто проверям наличие одноименных узлов без атрибута "Имя".
                    if sub_elem.tag in names_check["main"]:
                        raise ExtException(message='Дублирующиеся узлы в xml файле.',
                                           dump=f'{sub_elem.tag}.{item_name}')
                    names_check["main"].append(sub_elem.tag)
                    if isinstance(value, str):
                        d.append(value)
                    else:
                        value_new = OrderedDict()  # Для порядка Имя-Значение в результате делаем новый результат.
                        value_new["Имя"] = sub_elem.tag
                        value_new.update(value)
                        # for value_key in value.keys():
                        #     value_new[value_key] = value[value_key]
                        d.append(value_new)
                else:
                    d[sub_elem.tag] = value
        return d

    @classmethod
    def update_element_in_dict(cls, _data, _path, _value):
        _num = re.compile(r'^\d+$')
        _path = _path.split('.')
        current = _data
        size = len(_path)
        for i, elem in enumerate(_path):
            if _num.match(elem):
                elem = int(elem)
            if i == size - 1:
                current[elem] = _value
            else:
                current = current[elem]

    @classmethod
    def get_element_in_dict(cls, _data, _path, default=None):
        _num = re.compile(r'^\d+$')
        _path = _path.split('.')
        current = _data
        try:
            for i, elem in enumerate(_path):
                if _num.match(elem):
                    elem = int(elem)
                current = current[elem]
        except KeyError:
            return default
        return current

    @classmethod
    def compare(cls, base, new):
        if isinstance(base, dict):
            difference = False
            res = {}
            for elem in new:
                try:
                    if base and elem in base:
                        if isinstance(new[elem], dict):
                            _difference, _res = cls.compare(base[elem], new[elem])
                            if _difference:
                                difference = True
                                res[elem] = copy.deepcopy(_res)
                        else:
                            if new[elem] != base[elem]:
                                difference = True
                                res[elem] = new[elem]
                    else:
                        difference = True
                        res[elem] = new[elem]
                except Exception as e:
                    raise Exception('compare: {0}'.format(str(e)), elem)
        else:
            difference = False
            res = None
            if base != new:
                difference = True
                res = new
        return difference, res

    @classmethod
    def get_default_config(cls, current_class, root_class, cache):
        _type = root_class.__name__
        try:
            return cache['{0}_{1}'.format(_type, cls.__name__)]
        except KeyError:
            pass
        schema = {}

        for elem in current_class.__bases__:
            if issubclass(elem, root_class):
                try:
                    _schema = cache['{0}_{1}'.format(_type, elem.__name__)]
                except KeyError:
                    _schema = cls.get_default_config(elem, root_class, cache)
                    cache['res' + elem.__name__] = Helper.update_dict({}, _schema)
                Helper.update_dict(schema, _schema)
        if hasattr(current_class, 'file'):
            config_path = '{0}/{1}.json'.format(os.path.dirname(current_class.file), current_class.__name__)
            try:
                with open(config_path, 'r', encoding='utf-8') as file:
                    _schema = json.load(file)
                    Helper.update_dict(schema, _schema)
            except FileNotFoundError:
                return schema
            except Exception as e:
                pass
        cache['{0}_{1}'.format(_type, current_class.__name__)] = Helper.update_dict({}, schema)
        return schema

    @staticmethod
    def copy_via_json(config):
        return json.loads(json.dumps(config))

    @staticmethod
    def add_to_object_if_exist(src_obj: dict, key_name: str, dest_obj: dict, *, new_name: str = None,
                               only_filled: bool = True):
        try:
            value = src_obj[key_name]
        except (KeyError, TypeError):
            return
        if only_filled and not value:
            return
        dest_obj[key_name if new_name is None else new_name] = value

    @staticmethod
    def to_camel_case(text):
        s = text.replace("-", " ").replace("_", " ")
        s = s.split()
        if len(text) == 0:
            return text
        return ''.join(i.capitalize() for i in s)

    @staticmethod
    def obj_set_path_value(obj, obj_path, value, *, delimiter=None, skip_if_none=False, serializer=None):
        if skip_if_none and value is None:
            return
        if serializer:
            value = serializer(value)
        if delimiter:
            _path = obj_path.split(delimiter)
            obj = Helper.obj_get_path_value(obj, _path[:-1], delimiter=delimiter)
            obj[_path[-1]] = value
        else:
            obj[obj_path] = value

    @staticmethod
    def obj_get_path_value(obj, obj_path, *, delimiter=None):
        if isinstance(obj_path, str):
            if delimiter:
                _path = obj_path.split(delimiter)
            else:
                _path = [obj_path]
        else:
            _path = obj_path
        _obj = obj
        try:
            i = 0
            size = len(_path)
            while i < size:
                elem = _path[i]
                if isinstance(_obj, dict):
                    _obj = _obj.get(elem)
                elif isinstance(_obj, list):
                    if elem.isnumeric():  # это число
                        _obj = _obj[int(elem)]
                    else:  # конструкция для поиски значения в таблице
                        # первое значение имя поля по которому ищем, следующее его значение
                        # получаем в контекст объкт строки таблицы
                        index = ArrayHelper.find_by_key(_obj, _path[i + 1], elem)
                        if index >= 0:
                            _obj = _obj[index]
                            i += 1
                        else:
                            return None
                # else:
                #     return None
                if not _obj:
                    break
                i += 1
            return _obj

        except AttributeError:
            if obj:
                raise Exception(f'obj_get_path_value: not object')
            else:
                raise Exception(f'Object obj_get_path_value: not defined')


def async_test(f):
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        if inspect.iscoroutinefunction(f):
            future = f(*args, **kwargs)
        else:
            coroutine = asyncio.coroutine(f)
            future = coroutine(*args, **kwargs)
        loop.run_until_complete(future)

    return wrapper


def convert_ticks_to_datetime(ticks):
    return datetime.datetime(1, 1, 1) + datetime.timedelta(microseconds=ticks // 10)


def get_tzinfo(timezone_offset=+3.0):
    return datetime.timezone(datetime.timedelta(hours=timezone_offset))


def version_to_string(version, **kwargs):
    digits = version.split('.')
    result = ''
    for i in range(len(digits)):
        size = kwargs.get(f'size{i + 1}', 3)
        if size:
            result += f'{int(digits[i]):0{size}}'
    return result


