import urllib.parse

from .ExtException import ExtException
from .Helper import Helper


class JsonSchema4:
    def __init__(self, loader=None, cache=None):
        self.loader = loader
        self.cache = {} if cache is None else cache
        self.data = {}
        self.id = None
        self.uri = None
        self.version = None
        self.load_history = []

    def load_from_uri(self, uri, **kwargs):
        try:
            uri = urllib.parse.urlparse(uri)  # (scheme, netloc, path, params, query, fragment)
            _id = self.get_id_from_uri(uri, self.id)

            if _id not in self.cache:
                JsonSchema4.load_from_file(_id, loader=self.loader, cache=self.cache)
            if not uri[5]:
                try:
                    return self.cache[_id]['data']
                except KeyError:
                    raise Exception('bad schema id or definition in {}'.format(_id))

            _fragment = uri[5].split('/')[1:]
            _result = self.cache[_id]
            for elem in _fragment:
                _result = _result[elem]
            return _result
        except Exception as err:
            raise ExtException(
                action='JsonSchemaLoaderMixin.load_from_uri',
                dump={'uri': uri},
                parent=err) from err

    @classmethod
    def load_from_file(cls, file_name, *, loader=None, cache=None):
        try:
            self = cls(loader, cache)
            _path = None
            raw = self.loader.load(file_name)
            # for _dir in self.dir:
            #     _path = '{0}/{1}'.format(_dir, file_name)
            #     if os.path.isfile(_path):
            #         break
            #     else:
            #         _path = None
            # if _path is None:
            #     raise ExtException(message='Json schema file not found', detail=file_name)
            #
            # with open(_path, 'r', encoding='utf-8') as file:
            #     try:
            #         raw = json.load(file)
            #     except Exception as err:
            #         raise ExtException(message='JsonSchema not load from file',
            #                            detail=f'{file_name} {str(err)}') from err
            self.load(raw)
            return self.cache[self.id]['data']
        except Exception as err:
            raise ExtException(
                action='JsonSchemaLoaderMixin.load_from_file',
                dump={'file_name': file_name},
                parent=err) from err

    def load_from_rt(self, rt):
        schema = {}
        for name in rt:
            uri = '{0}.json'.format(name)
            _schema = self.load_from_uri(uri)
            Helper.update_dict(schema, _schema)
        return schema

    @staticmethod
    def get_id_from_uri(uri, default=None):
        if uri[2]:
            return uri[2].split('/')[-1][:-5]
        elif default:
            return default
        raise Exception('not define scheme id')

    def load(self, schema):
        try:
            try:
                self.version = urllib.parse.urlparse(schema['$schema'])[2].split('/')[0]
            except KeyError:
                self.version = 4
            self.id = self.get_id_from_uri(urllib.parse.urlparse(schema['id']))
            self.cache[self.id] = dict(data=dict(), definitions=dict())
            if 'definitions' in schema:
                for tmpl in schema['definitions']:
                    self.cache[self.id]['definitions'][tmpl] = dict()
                    for props in schema['definitions'][tmpl]:
                        _type = schema['definitions'][tmpl][props].__class__.__name__
                        self.load_elem(
                            self.cache[self.id]['definitions'][tmpl],
                            schema['definitions'][tmpl][props],
                            props
                        )
            for elem in schema:
                if elem != 'definitions':
                    self.load_elem(self.cache[self.id]['data'], schema[elem], elem)
            pass
        except Exception as err:
            raise ExtException(
                action='JsonSchemaLoaderMixin.load',
                parent=err) from err

    # @staticmethod
    # def add_prop(data, node, name, default=None):
    #     try:
    #         data[name] = node['name']
    #     except KeyError:
    #         if default is not None:
    #             data[name] = default

    def load_elem_ref(self, data, value, name):
        res = self.load_from_uri(value)
        Helper.update_dict(data, res)

    def load_elem(self, data, value, name):
        try:
            value_type = value.__class__.__name__
            getattr(self, f'load_elem_{value_type}')(
                data, value, name)
        except Exception as err:
            raise ExtException(
                action='JsonSchemaLoaderMixin.load_elem',
                dump={'elem_name': name},
                parent=err) from err
        pass

    def load_elem_str(self, data, value, name):
        if name != '$ref':
            data[name] = value
            return
        self.load_elem_ref(data, value, name)

    def load_elem_dict(self, data, value, name):
        if name not in data:
            data[name] = dict()
        for elem in value:
            self.load_elem(data[name], value[elem], elem)

    def load_elem_list(self, data, value, name):
        if name == 'allOf':
            for elem in value:
                for _name in elem:
                    self.load_elem(data, elem[_name], _name)
            return
        else:
            if name not in data:
                data[name] = value
            else:
                data[name] = list(set(data[name] + value))
        pass

    def load_elem_bool(self, data, value, name):
        data[name] = value

    def load_elem_int(self, data, value, name):
        data[name] = value

    def load_elem_float(self, data, value, name):
        data[name] = value
